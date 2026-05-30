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

## Steps

For Kali Linux / Ubuntu / Debian:

```bash
1) sudo apt update

2) sudo apt install python3 python3-pip python3-venv nmap -y

3) sudo apt install sqlite3 libsqlite3-dev sqlitebrowser -y

4) python3 -m venv venv

5) source venv/bin/activate

6) pip install -r requirements.txt

Now your network-scanner is ready to go.
```

## Usage

### Basic Scan

Perform a normal scan against a target:

```bash
python3 main.py --target 192.168.1.1
```

### Quick Scan

Scans common ports and performs service/version detection.

```bash
python3 main.py --target 192.168.1.1 --scan-type quick
```

### Full Port Scan

Scans all ports from 1 to 65535.

```bash
python3 main.py --target 192.168.1.1 --scan-type full
```

### Active Host Discovery

Discover active hosts without performing port scans.

```bash
python3 main.py --target 192.168.1.0/24 --discover
```

### Custom Port Scan

Scan specific ports only.

```bash
python3 main.py --target 192.168.1.1 --ports 22,80,443
```

### No Ping Scan

Useful when ICMP ping is blocked.

```bash
python3 main.py --target 192.168.1.1 --no-ping
```

### Generate Reports

Generate HTML report only:

```bash
python3 main.py --target 192.168.1.1 --output html
```

Generate JSON report only:

```bash
python3 main.py --target 192.168.1.1 --output json
```

Generate CSV report only:

```bash
python3 main.py --target 192.168.1.1 --output csv
```

Generate all report formats:

```bash
python3 main.py --target 192.168.1.1 --output all
```

## Advanced Scan Modes

The following scan modes require root privileges.

### OS Detection

```bash
sudo $(which python) main.py --target 192.168.1.1 --scan-type os
```

### Stealth Scan

```bash
sudo $(which python) main.py --target 192.168.1.1 --scan-type stealth
```

### UDP Scan

```bash
sudo $(which python) main.py --target 192.168.1.1 --scan-type udp
```

### Aggressive Scan

```bash
sudo $(which python) main.py --target 192.168.1.1 --scan-type aggressive
```

---

## Database Usage

NetShield automatically creates a SQLite database named:

```text
netshield.db
```

The database is created automatically during the first scan execution.

Example:

```bash
python3 main.py --target 127.0.0.1
```

After the first successful scan, the file `netshield.db` will appear in the project directory.

### View Scan History

```bash
python3 history.py
```

This displays previously saved scan results.

### Open Database Using SQLite Browser

Install SQLite Browser:

```bash
sudo apt install sqlitebrowser -y
```

Launch it:

```bash
sqlitebrowser netshield.db
```

Or:

```bash
sqlitebrowser
```

Then open:

```text
netshield.db
```

### View Database Using Terminal

```bash
sqlite3 netshield.db
```

Show tables:

```sql
.tables
```

View saved scans:

```sql
SELECT * FROM scans;
```

Exit SQLite:

```sql
.quit
```

---

## Reports

Generated reports are stored automatically inside:

```text
reports/
```

Supported report formats:

* HTML
* JSON
* CSV

---

## Screenshots

Screenshots demonstrating the tool can be found in the `Screenshots/` directory.

---

## Security Notice

This tool is intended for educational purposes and authorized security assessments only.

Only scan systems and networks that you own or have explicit permission to test.
