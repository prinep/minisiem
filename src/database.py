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
                rule TEXT
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
            INSERT INTO alerts (message, severity, ip, rule)
            VALUES (?, ?, ?, ?)
        """, (
            alert.message,
            alert.severity,
            alert.ip,
            alert.rule
        ))

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
            SELECT message, severity, ip, rule
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

        