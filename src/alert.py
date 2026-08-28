class Alert:
    def __init__(self, message, severity, ip, rule, risk_score):
        self.message = message
        self.severity = severity
        self.ip = ip
        self.rule = rule
        self.risk_score = risk_score