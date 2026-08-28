class Dashboard:
    def __init__(self, database):
        self.database = database

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
            print("[4] Exit")

            choice = input("\nChoose an option: ")

            if choice == "4":
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

            else:
                print("Invalid option.")
        