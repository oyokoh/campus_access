
"""Command-line interface for the campus access-card manager."""

from campus_access.work import RequestManager
from campus_access.errors import RequestError, DataError
from campus_access.storage import save_manager, load_manager

DATA_FILE = "data/requests.json"


def main():
    manager = RequestManager()

    while True:
        print("\nCampus Access-Card Manager")
        print("1. Create request")
        print("2. View request")
        print("3. Approve request")
        print("4. Issue card")
        print("5. Return card")
        print("6. List requests")
        print("7. Save requests")
        print("8. Reload requests")
        print("9. Exit")

        try:
            choice = input("Choose an option: ").strip()

            if choice == "1":
                fellow_id = input("Enter fellow ID: ").strip()
                card_type = input(
                    "Enter card type (visitor, student, staff): "
                ).strip()

                request = manager.create(fellow_id, card_type)
                print("Request created:", request)

            elif choice == "2":
                request_id = input("Enter request ID: ").strip()
                print(manager.view(request_id))

            elif choice == "3":
                request_id = input("Enter request ID: ").strip()
                approver = input("Enter approver name: ").strip()
                print(manager.approve(request_id, approver))

            elif choice == "4":
                request_id = input("Enter request ID: ").strip()
                print(manager.issue(request_id))

            elif choice == "5":
                request_id = input("Enter request ID: ").strip()
                print(manager.return_card(request_id))

            elif choice == "6":
                status = input(
                    "Filter by status (requested, approved, issued, returned), "
                    "or press Enter for all: "
                ).strip()

                print(manager.list(status if status else None))

            elif choice == "7":
                save_manager(manager, DATA_FILE)
                print("Requests saved successfully.")

            elif choice == "8":
                manager = load_manager(DATA_FILE)
                print("Requests reloaded successfully.")

            elif choice == "9":
                print("Goodbye.")
                break

            else:
                print("Invalid option. Choose a number from 1 to 9.")

        except (RequestError, DataError) as error:
            print("Error:", error)

        except (EOFError, KeyboardInterrupt):
            print("\nExiting program.")
            break


if __name__ == "__main__":
    main()