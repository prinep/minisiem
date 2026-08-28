import sqlite3


class Database:
    def __init__(self, db_name="minisiem.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                event TEXT,
                username TEXT,
                ip TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT,
                severity TEXT,
                ip TEXT,
                rule TEXT,
                risk_score INTEGER
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,
                risk_score INTEGER,
                alert_count INTEGER
            )
        """)

    def save_event(self, event):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO events (timestamp, event, username, ip)
            VALUES (?, ?, ?, ?)
        """, (
            event.timestamp,
            event.event,
            event.username,
            event.ip
        ))

        self.connection.commit()

    def save_alert(self, alert):
        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO alerts (message, severity, ip, rule, risk_score)
            VALUES (?, ?, ?, ?, ?)
        """, (
            alert.message,
            alert.severity,
            alert.ip,
            alert.rule,
            alert.risk_score
        ))
    def save_incident(self, ip, risk_score, alert_count):
        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE incidents
            SET risk_score = ?, alert_count = ?
            WHERE ip = ?
        """, (
            risk_score,
            alert_count,
            ip
        ))

        if cursor.rowcount == 0:
            cursor.execute("""
                INSERT INTO incidents (ip, risk_score, alert_count)
                VALUES (?, ?, ?)
            """, (
                ip,
                risk_score,
                alert_count
            ))

        self.connection.commit()

    def get_incidents(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT ip, risk_score, alert_count
            FROM incidents
            ORDER BY risk_score DESC
        """)

        return cursor.fetchall()

    def get_recent_events(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT timestamp, event, username, ip
            FROM events
            ORDER BY id DESC
            LIMIT 20
        """)

        return cursor.fetchall()

    def get_alerts(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT message, severity, ip, rule, risk_score
            FROM alerts
            ORDER BY id DESC
            LIMIT 20
        """)

        return cursor.fetchall()

    def get_statistics(self):
        cursor = self.connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM events")
        total_events = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM alerts")
        total_alerts = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity = 'HIGH'")
        high_alerts = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity = 'CRITICAL'")
        critical_alerts = cursor.fetchone()[0]

        return total_events, total_alerts, high_alerts, critical_alerts
    def get_alert_count(self):
                    cursor = self.connection.cursor()
    
                    cursor.execute("SELECT COUNT(*) FROM alerts")
    
                    return cursor.fetchone()[0]

        