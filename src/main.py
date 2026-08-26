from parser import parse_log


with open("logs/sample.log", "r") as file:
    logs = file.readlines()


for log in logs:
    event = parse_log(log)

    if event:
        print(event.ip)
