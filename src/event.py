class LogEvent:
    def __init__(self, timestamp, event, username, ip):
        self.timestamp = timestamp
        self.event = event
        self.username = username
        self.ip = ip