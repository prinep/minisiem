import glob
from parser import parse_log
from detector import DetectionEngine
from database import Database
from dashboard import Dashboard


detector = DetectionEngine()
database = Database()

log_files = glob.glob("logs/*.log")

for log_file in log_files:
        with open(log_file, "r") as file:
            logs = file.readlines()

        for log in logs:
            event = parse_log(log)

            if event:
                database.save_event(event)

                alerts = detector.analyze(event)

                for alert in alerts:

                    database.save_alert(alert)
                    incident = detector.correlate_alert(alert)
                    database.save_incident(
                        alert.ip,
                        incident["risk_score"],
                        len(incident["alerts"])
                    )

                    print("Incident Risk:", incident["risk_score"])
                    print("Alerts in Incident:", len(incident["alerts"]))
                    
                    print("ALERT:", alert.message)
                    print("Severity:", alert.severity)
                    print("IP:", alert.ip)
                    print("Rule:", alert.rule)
                    print("Risk Score:", alert.risk_score)
                    print()
dashboard = Dashboard(database, detector)
dashboard.show_menu()