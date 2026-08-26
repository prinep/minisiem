from parser import parse_log
from detector import DetectionEngine


detector = DetectionEngine()

with open("logs/sample.log", "r") as file:
    logs = file.readlines()


for log in logs:
    event = parse_log(log)

    if event:
        alerts = detector.analyze(event)

        for alert in alerts:
            print("ALERT:", alert.message)
            print("Severity:", alert.severity)
            print("IP:", alert.ip)
            print("Rule:", alert.rule)
            print()