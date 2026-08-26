from parser import parse_log
from detector import DetectionEngine
from database import Database


detector = DetectionEngine()
database = Database()

with open("logs/sample.log", "r") as file:
    logs = file.readlines()


for log in logs:
    event = parse_log(log)

    if event:
        database.save_event(event)

        alerts = detector.analyze(event)

        for alert in alerts:

            database.save_alert(alert)
            
            print("ALERT:", alert.message)
            print("Severity:", alert.severity)
            print("IP:", alert.ip)
            print("Rule:", alert.rule)
            print()