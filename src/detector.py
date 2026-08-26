class DetectionEngine:
    def __init__(self):
        self.failed_attempts = {}
        self.alerted_ips = set()
        self.brute_force_ips = set()

    def analyze(self, event):
        ip = event.ip

        if event.event == "Failed":
            if ip not in self.failed_attempts:
                self.failed_attempts[ip] = 0

            self.failed_attempts[ip] += 1

            if self.failed_attempts[ip] >= 3 and ip not in self.alerted_ips:
                self.alerted_ips.add(ip)
                self.brute_force_ips.add(ip)

                return f"Brute-force attack detected from {ip}"

        elif event.event == "Accepted":
            if ip in self.brute_force_ips:
                return f"Successful login after brute-force attempt from {ip}"

        return None