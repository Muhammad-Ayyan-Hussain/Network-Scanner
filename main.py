import argparse
import os

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from netshield.scanner import build_scan_arguments, discover_hosts, scan_host
from netshield.vulnerability import check_vulnerability
from netshield.database import connect_database, save_scan
from netshield.report import (
    generate_html_report,
    generate_json_report,
    generate_csv_report
)

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="NetShield - Advanced Linux Network Scanner and Vulnerability Reporter"
    )

    parser.add_argument("--target", required=True, help="Target IP or range")

    parser.add_argument(
        "--scan-type",
        choices=["quick", "normal", "full", "stealth", "udp", "os", "aggressive"],
        default="normal",
        help="Scan type"
    )

    parser.add_argument("--ports", help="Custom ports example: 22,80,443 or 1-1000")

    parser.add_argument(
        "--timing",
        choices=["T0", "T1", "T2", "T3", "T4", "T5"],
        default="T3",
        help="Timing template"
    )

    parser.add_argument(
        "--output",
        choices=["html", "json", "csv", "all"],
        default="all",
        help="Report output format"
    )

    parser.add_argument("--no-ping", action="store_true", help="Skip ping discovery")

    parser.add_argument(
        "--discover",
        action="store_true",
        help="Only discover active hosts"
    )

    args = parser.parse_args()

    target = args.target
    scan_type = args.scan_type
    custom_ports = args.ports
    timing = args.timing
    output_format = args.output
    no_ping = args.no_ping
    discover_only = args.discover

    if scan_type in ["stealth", "udp", "os", "aggressive"] and os.geteuid() != 0:
        console.print("[yellow]Warning: This scan type may require sudo/root privileges.[/yellow]")

    conn, cursor = connect_database()

    scan_arguments = build_scan_arguments(
        scan_type=scan_type,
        custom_ports=custom_ports,
        timing=timing,
        no_ping=no_ping
    )

    console.print(f"\n[bold cyan]Target:[/bold cyan] {target}")
    console.print(f"[bold cyan]Scan Type:[/bold cyan] {scan_type}")
    console.print(f"[bold cyan]Timing:[/bold cyan] {timing}")
    console.print(f"[bold cyan]Output:[/bold cyan] {output_format}")
    console.print(f"[bold cyan]No Ping:[/bold cyan] {no_ping}")
    console.print(f"[bold cyan]Discovery Only:[/bold cyan] {discover_only}")
    console.print(f"[bold cyan]Nmap Arguments:[/bold cyan] {scan_arguments}\n")

    hosts = discover_hosts(target, no_ping=no_ping)

    if not hosts:
        console.print("[red]No live hosts found.[/red]")
        conn.close()
        return

    live_table = Table(title="Live Hosts")
    live_table.add_column("IP Address", style="cyan")
    live_table.add_column("Status", style="green")

    for host in hosts:
        live_table.add_row(host, "up")

    console.print(live_table)

    if discover_only:
        console.print("\n[bold green]Discovery scan completed successfully.[/bold green]")
        conn.close()
        return

    report_results = []

    for host in hosts:
        console.print(f"\n[bold yellow]Scanning Ports on {host}[/bold yellow]\n")

        scanner = scan_host(host, scan_arguments)

        if scanner is None:
            console.print(f"[red]Skipping {host} because scan failed.[/red]")
            continue

        host_data = {
            "ip": host,
            "os": "Unknown",
            "ports": [],
            "vulnerabilities": []
        }

        port_table = Table(title=f"Open Ports - {host}")
        port_table.add_column("Port", style="cyan")
        port_table.add_column("Protocol", style="magenta")
        port_table.add_column("Service", style="green")
        port_table.add_column("State", style="red")
        port_table.add_column("Version", style="yellow")

        vuln_table = Table(title=f"Vulnerabilities Found - {host}")
        vuln_table.add_column("Port", style="cyan")
        vuln_table.add_column("Issue", style="red")
        vuln_table.add_column("Severity", style="yellow")
        vuln_table.add_column("Recommendation", style="green")

        vulnerabilities_found = False

        if host not in scanner.all_hosts():
            console.print(f"[red]No scan results for {host}[/red]")
            continue

        os_info = "Unknown"

        if "osmatch" in scanner[host] and scanner[host]["osmatch"]:
            os_info = scanner[host]["osmatch"][0].get("name", "Unknown")

        host_data["os"] = os_info

        console.print(f"[bold blue]Detected OS:[/bold blue] {os_info}")

        for proto in scanner[host].all_protocols():
            ports = sorted(scanner[host][proto].keys())

            for port in ports:
                service = scanner[host][proto][port].get("name", "unknown")
                state = scanner[host][proto][port].get("state", "unknown")

                product = scanner[host][proto][port].get("product", "")
                version = scanner[host][proto][port].get("version", "")
                extra_info = scanner[host][proto][port].get("extrainfo", "")

                service_version = f"{product} {version} {extra_info}".strip()

                if not service_version:
                    service_version = "Unknown"

                issue, severity, recommendation = check_vulnerability(port, state)

                port_table.add_row(
                    str(port),
                    proto,
                    service,
                    state,
                    service_version
                )

                if severity != "None":
                    vulnerabilities_found = True

                    vuln_table.add_row(
                        str(port),
                        issue,
                        severity,
                        recommendation
                    )

                    host_data["vulnerabilities"].append({
                        "port": port,
                        "name": issue,
                        "severity": severity,
                        "recommendation": recommendation
                    })

                host_data["ports"].append({
                    "port": port,
                    "protocol": proto,
                    "service": service,
                    "state": state,
                    "version": service_version
                })

                save_scan(
                    cursor,
                    conn,
                    target,
                    host,
                    port,
                    proto,
                    service,
                    state,
                    service_version,
                    severity,
                    recommendation
                )

        console.print(port_table)

        if vulnerabilities_found:
            console.print(vuln_table)
        else:
            console.print(Panel.fit("[green]No common vulnerabilities detected.[/green]"))

        report_results.append(host_data)

    if output_format in ["html", "all"]:
        html_report = generate_html_report(
            target,
            scan_type,
            custom_ports,
            report_results
        )
        console.print(f"\n[bold green]HTML report generated:[/bold green] {html_report}")

    if output_format in ["json", "all"]:
        json_report = generate_json_report(
            target,
            scan_type,
            custom_ports,
            report_results
        )
        console.print(f"[bold green]JSON report generated:[/bold green] {json_report}")

    if output_format in ["csv", "all"]:
        csv_report = generate_csv_report(report_results)
        console.print(f"[bold green]CSV report generated:[/bold green] {csv_report}")

    console.print("[bold green]Scan results saved to database:[/bold green] netshield.db")

    conn.close()


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user.")

    except Exception as error:
        print(f"\n[!] Unexpected error: {error}")
