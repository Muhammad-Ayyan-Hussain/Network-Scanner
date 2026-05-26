# NetShield

NetShield is an advanced Linux-based Network Scanner and Vulnerability Reporting Tool built with Python and Nmap.

It is designed for Information Assurance, cybersecurity learning, and authorized network auditing.

## Features

- Active host discovery
- Port scanning
- Full port scan support
- Service detection
- Version detection
- OS detection
- Vulnerability rule matching
- Risk severity classification
- HTML report generation
- JSON report generation
- CSV report generation
- SQLite scan history
- Timing templates
- Custom port scanning
- No-ping scan mode
- Keyboard interrupt handling
- Error handling

## Project Structure

```text
NetShield/
│
├── netshield/
│   ├── __init__.py
│   ├── scanner.py
│   ├── vulnerability.py
│   ├── database.py
│   └── report.py
│
├── reports/
├── main.py
├── history.py
├── requirements.txt
├── README.md
└── Screenshots
```
# Environment Setup and Dependency Installation

## Steps — Update System Packages

For Kali Linux / Ubuntu / Debian:

```bash
1) sudo apt update

2) sudo apt install python3 python3-pip python3-venv nmap -y

3) sudo apt install sqlite3 libsqlite3-dev sqlitebrowser -y

4) python3 -m venv venv

5) source venv/bin/activate

6) pip install -r requirements.txt


7) python3 main.py --target 192.168.10.1 --scan-type quick

8) For OS,UDP,Aggressive,Stealth Scan,etc. Use  sudo $(which python) main.py --target 192.168.1.1 --scan-type os (for OS)

9) sudo $(which python) main.py --target 192.168.1.1 --scan-type aggressive (for aggressive scan and so on)
