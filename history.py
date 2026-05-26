import sqlite3
from rich.console import Console
from rich.table import Table

console = Console()


def main():
    conn = sqlite3.connect("netshield.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, target, host, port, protocol, service, state, version, severity, scan_date
    FROM scans
    ORDER BY scan_date DESC
    LIMIT 50
    """)

    rows = cursor.fetchall()

    if not rows:
        console.print("[red]No scan history found.[/red]")
        conn.close()
        return

    table = Table(title="NetShield Scan History")

    table.add_column("ID", style="cyan")
    table.add_column("Target", style="green")
    table.add_column("Host", style="green")
    table.add_column("Port", style="cyan")
    table.add_column("Protocol", style="magenta")
    table.add_column("Service", style="yellow")
    table.add_column("State", style="red")
    table.add_column("Version", style="blue")
    table.add_column("Severity", style="bold red")
    table.add_column("Date", style="white")

    for row in rows:
        table.add_row(*[str(item) for item in row])

    console.print(table)
    conn.close()


if __name__ == "__main__":
    main()
