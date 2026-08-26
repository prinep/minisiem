import re

with open("logs/sample.log", "r") as file:
    logs = file.readlines()

for log in logs:
    match = re.search(
        r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) sshd: (Failed|Accepted) password for (\w+) from (\d+\.\d+\.\d+\.\d+)",
        log
    )

    if match:
        timestamp = match.group(1)
        event = match.group(2)
        username = match.group(3)
        ip = match.group(4)

        print("Timestamp:", timestamp)
        print("Event:", event)
        print("Username:", username)
        print("IP:", ip)
        print()