from alert import Alert


class DetectionEngine:
    def __init__(self):
        self.failed_attempts = {}
        self.alerted_ips = set()
        self.brute_force_ips = set()

    def check_brute_force(self, event):
        if event.event != "Failed":
            return None

        ip = event.ip

        if ip not in self.failed_attempts:
            self.failed_attempts[ip] = 0

        self.failed_attempts[ip] += 1

        if self.failed_attempts[ip] >= 3 and ip not in self.alerted_ips:
            self.alerted_ips.add(ip)
            self.brute_force_ips.add(ip)

            return Alert(
                "Brute-force attack detected",
                "HIGH",
                ip,
                "BRUTE_FORCE"
            )

        return None

    def check_brute_force_success(self, event):
        if event.event == "Accepted" and event.ip in self.brute_force_ips:
            return Alert(
                "Successful login after brute-force attempt",
                "CRITICAL",
                event.ip,
                "BRUTE_FORCE_SUCCESS"
            )

        return None

    def check_unusual_login_time(self, event):
        if event.event != "Accepted":
            return None

        hour = int(event.timestamp[11:13])

        if hour < 6 or hour >= 22:
            return Alert(
                "Login outside normal hours",
                "MEDIUM",
                event.ip,
                "UNUSUAL_LOGIN_TIME"
            )

        return None

    def analyze(self, event):
        checks = [
            self.check_brute_force,
            self.check_brute_force_success,
            self.check_unusual_login_time
        ]

        alerts = []

        for check in checks:
            alert = check(event)

            if alert:
                alerts.append(alert)

        return alerts