class Alert:
    def __init__(self, message, severity, ip, rule):
        self.message = message
        self.severity = severity
        self.ip = ip
        self.rule = rule