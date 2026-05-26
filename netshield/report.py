import os
import json
import csv

from datetime import datetime
from jinja2 import Template


def generate_html_report(target, scan_type, ports, results):

    os.makedirs("reports", exist_ok=True)

    html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>NetShield Scan Report</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f6f8;
            padding: 20px;
            color: #222;
        }

        h1 {
            color: #111;
        }

        h2, h3 {
            color: #222;
        }

        .summary {
            background: white;
            padding: 15px;
            border-left: 5px solid #222;
            margin-bottom: 20px;
        }

        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 25px;
            background: white;
        }

        th, td {
            border: 1px solid #ccc;
            padding: 10px;
            text-align: left;
        }

        th {
            background-color: #222;
            color: white;
        }

        .Critical {
            color: red;
            font-weight: bold;
        }

        .High {
            color: darkred;
            font-weight: bold;
        }

        .Medium {
            color: orange;
            font-weight: bold;
        }

        .Low {
            color: green;
            font-weight: bold;
        }

        .None {
            color: gray;
        }
    </style>
</head>

<body>

    <h1>NetShield Vulnerability Report</h1>

    <div class="summary">
        <p><strong>Target:</strong> {{ target }}</p>
        <p><strong>Date:</strong> {{ date }}</p>
        <p><strong>Scan Type:</strong> {{ scan_type }}</p>
        <p><strong>Custom Ports:</strong> {{ ports }}</p>
        <p><strong>Total Hosts Found:</strong> {{ results|length }}</p>
    </div>

    {% for host in results %}

        <h2>Host: {{ host.ip }}</h2>

        <h3>Open Ports</h3>

        <table>
            <tr>
                <th>Port</th>
                <th>Protocol</th>
                <th>Service</th>
                <th>State</th>
                <th>Version</th>
            </tr>

            {% for port in host.ports %}
            <tr>
                <td>{{ port.port }}</td>
                <td>{{ port.protocol }}</td>
                <td>{{ port.service }}</td>
                <td>{{ port.state }}</td>
                <td>{{ port.version }}</td>
            </tr>
            {% endfor %}
        </table>

        <h3>Vulnerability Findings</h3>

        {% if host.vulnerabilities %}

        <table>
            <tr>
                <th>Port</th>
                <th>Issue</th>
                <th>Severity</th>
                <th>Recommendation</th>
            </tr>

            {% for vuln in host.vulnerabilities %}
            <tr>
                <td>{{ vuln.port }}</td>
                <td>{{ vuln.name }}</td>
                <td class="{{ vuln.severity }}">{{ vuln.severity }}</td>
                <td>{{ vuln.recommendation }}</td>
            </tr>
            {% endfor %}
        </table>

        {% else %}
            <p>No common vulnerabilities detected.</p>
        {% endif %}

    {% endfor %}

</body>
</html>
"""

    template = Template(html_template)

    html_content = template.render(
        target=target,
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        scan_type=scan_type,
        ports=ports if ports else "Default Nmap ports",
        results=results
    )

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    report_file = f"reports/scan_report_{timestamp}.html"

    with open(report_file, "w") as file:
        file.write(html_content)

    return report_file


def generate_json_report(target, scan_type, ports, results):

    os.makedirs("reports", exist_ok=True)

    data = {
        "tool": "NetShield",
        "target": target,
        "scan_type": scan_type,
        "ports": ports if ports else "Default Nmap ports",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": results
    }

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    report_file = f"reports/scan_report_{timestamp}.json"

    with open(report_file, "w") as file:
        json.dump(data, file, indent=4)

    return report_file


def generate_csv_report(results):

    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    report_file = f"reports/scan_report_{timestamp}.csv"

    with open(report_file, "w", newline="") as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow([
            "Host",
            "Port",
            "Protocol",
            "Service",
            "State",
            "Version"
        ])

        for host in results:

            for port in host["ports"]:

                writer.writerow([
                    host["ip"],
                    port["port"],
                    port["protocol"],
                    port["service"],
                    port["state"],
                    port["version"]
                ])

    return report_file
