import sqlite3


def connect_database():
    conn = sqlite3.connect("netshield.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target TEXT,
        host TEXT,
        port INTEGER,
        protocol TEXT,
        service TEXT,
        state TEXT,
        version TEXT,
        severity TEXT,
        recommendation TEXT,
        scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    return conn, cursor


def save_scan(cursor, conn, target, host, port, protocol, service, state, version, severity, recommendation):
    cursor.execute("""
    INSERT INTO scans (
        target,
        host,
        port,
        protocol,
        service,
        state,
        version,
        severity,
        recommendation
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        target,
        host,
        port,
        protocol,
        service,
        state,
        version,
        severity,
        recommendation
    ))

    conn.commit()
