from alert import Alert


class DetectionEngine:
    def __init__(self):
        self.failed_attempts = {}
        self.alerted_ips = set()
        self.brute_force_ips = set()
        self.scanned_ports = {}
        self.port_scan_alerted = set()
        self.successful_logins = {}
        self.incidents = {}

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
                "BRUTE_FORCE",
                70
            )

        return None

    def check_brute_force_success(self, event):
        if event.event == "Accepted" and event.ip in self.brute_force_ips:
            return Alert(
                "Successful login after brute-force attempt",
                "CRITICAL",
                event.ip,
                "BRUTE_FORCE_SUCCESS",
                95
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
                "UNUSUAL_LOGIN_TIME",
                40
            )

        return None

    def check_path_traversal(self, event):
        if event.event.startswith("GET "):
            path = event.event[4:]

            suspicious_paths = [
                "/etc/passwd",
                "/etc/shadow",
                "../",
                "..\\"
            ]

            for suspicious in suspicious_paths:
                if suspicious in path:
                    return Alert(
                        "Possible path traversal attack",
                        "HIGH",
                        event.ip,
                        "PATH_TRAVERSAL",
                        80
                    )

        return None

    def check_port_scan(self, event):
        if event.event.startswith("PORT "):
            ip = event.ip
            port = event.event[5:]

            if ip not in self.scanned_ports:
                self.scanned_ports[ip] = set()

            self.scanned_ports[ip].add(port)

            if len(self.scanned_ports[ip]) >= 5 and ip not in self.port_scan_alerted:
                self.port_scan_alerted.add(ip)

                return Alert(
                    "Possible port scan detected",
                    "HIGH",
                    ip,
                    "PORT_SCAN",
                    75
                )

        return None
    def correlate_alert(self, alert):
        ip = alert.ip

        if ip not in self.incidents:
            self.incidents[ip] = {
                "alerts": [],
                "risk_score": 0
            }

        self.incidents[ip]["alerts"].append(alert)
        self.incidents[ip]["risk_score"] += alert.risk_score

        return self.incidents[ip]

    def analyze(self, event):
        checks = [
            self.check_brute_force,
            self.check_brute_force_success,
            self.check_unusual_login_time,
            self.check_path_traversal,
            self.check_port_scan
        ]

        alerts = []

        for check in checks:
            alert = check(event)

            if alert:
                alerts.append(alert)

        return alerts