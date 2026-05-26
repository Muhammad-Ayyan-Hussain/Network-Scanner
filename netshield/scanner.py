import nmap


def build_scan_arguments(scan_type, custom_ports=None, timing="T3", no_ping=False):

    scan_modes = {
        "quick": "-F -sV",
        "normal": "-sV",
        "full": "-p- -sV",
        "stealth": "-sS -sV",
        "udp": "-sU",
        "os": "-O",
        "aggressive": "-A"
    }

    scan_args = scan_modes.get(scan_type, "-sV")

    scan_args += f" -{timing}"

    if no_ping:
        scan_args += " -Pn"

    if custom_ports:
        scan_args += f" -p {custom_ports}"

    return scan_args


def discover_hosts(target, no_ping=False):

    scanner = nmap.PortScanner()

    try:

        if no_ping:
            scanner.scan(hosts=target, arguments="-Pn")
        else:
            scanner.scan(hosts=target, arguments="-sn")

        return scanner.all_hosts()

    except nmap.PortScannerError as error:
        print(f"[ERROR] Nmap error: {error}")
        return []

    except Exception as error:
        print(f"[ERROR] Discovery failed: {error}")
        return []


def scan_host(host, scan_arguments):

    scanner = nmap.PortScanner()

    try:

        scanner.scan(hosts=host, arguments=scan_arguments)

        return scanner

    except nmap.PortScannerError as error:
        print(f"[ERROR] Nmap scan error on {host}: {error}")
        return None

    except Exception as error:
        print(f"[ERROR] Scan failed on {host}: {error}")
        return None
