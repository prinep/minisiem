from parser import parse_log
from detector import DetectionEngine


detector = DetectionEngine()

with open("logs/sample.log", "r") as file:
    logs = file.readlines()


for log in logs:
    event = parse_log(log)

    if event:
        alert = detector.analyze(event)

        if alert:
            print("ALERT:", alert)
