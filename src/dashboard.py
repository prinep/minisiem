class Dashboard:
    def __init__(self, database):
        self.database = database

    def show_menu(self):
        while True:
            print("\n================================")
            print("           MiniSIEM")
            print("================================")
            print("1. View recent events")
            print("2. View alerts")
            print("3. Show statistics")
            print("4. Exit")

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
                        f"Rule: {alert[3]}"
                    )

            else:
                print("Invalid option.")