class Dashboard:
    def __init__(self, database, detector):
        self.database = database
        self.detector = detector

    def show_menu(self):
        while True:
            alert_count = self.database.get_alert_count()
            print("\n" + "=" * 50)
            print("                 MINISIEM")
            print("          Security Monitoring Tool")
            print("=" * 50)
            print(f"Active Alerts: {alert_count}")
            print("\n[1] View Recent Events")
            print("[2] View Security Alerts")
            print("[3] Security Statistics")
            print("[4] View Incidents")
            print("[5] Help")
            print("[6] Exit")

            choice = input("\nChoose an option: ")

            if choice == "6":
                print("Exiting MiniSIEM...")
                break
            elif choice == "1":
                events = self.database.get_recent_events()

                print("\n--- Recent Events ---")

                for event in events:
                    print(
                        f"{event[0]} | "
                        f"{event[1]} | "
                        f"{event[2]} | "
                        f"{event[3]}"
                    )
            elif choice == "2":
                alerts = self.database.get_alerts()

                print("\n--- Security Alerts ---")

                for alert in alerts:
                    print(
                        f"[{alert[1]}] "
                        f"{alert[0]} | "
                        f"IP: {alert[2]} | "
                        f"Rule: {alert[3]} | "
                        f"Risk: {alert[4]}"
                    )
            elif choice == "3":
                stats = self.database.get_statistics()

                print("\n--- Security Statistics ---")
                print("Total events:", stats[0])
                print("Total alerts:", stats[1])
                print("High alerts:", stats[2])
                print("Critical alerts:", stats[3])
            elif choice == "4":
                print("\n--- Security Incidents ---")

                if not self.detector.incidents:
                    print("No incidents detected.")
                else:
                    for ip, incident in self.detector.incidents.items():
                        print(f"\nIP: {ip}")
                        print(f"Risk Score: {incident['risk_score']}")
                        print(f"Alerts: {len(incident['alerts'])}")

                        for alert in incident["alerts"]:
                            print(f"  - {alert.rule} ({alert.severity})")
            elif choice == "5":
                print("\n--- MiniSIEM Help ---")
                print("1 - View the latest security events")
                print("2 - View detected security alerts")
                print("3 - View alert statistics")
                print("4 - View correlated security incidents")
                print("5 - Display this help message")
                print("6 - Exit MiniSIEM")
            else:
                print("Invalid option.")
        