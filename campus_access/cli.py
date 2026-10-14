from campus_access.work import RequestManager
from campus_access.errors import RequestError, DataError
from campus_access.storage import save_manager, load_manager


DATA_FILE = "data/requests.json"


def run():
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

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                fellow_id = input("Enter fellow ID: ")
                card_type = input(
                    "Enter card type (visitor/student/staff): "
                )

                request = manager.create(fellow_id, card_type)
                print("Request created:", request)

            elif choice == "2":
                request_id = input("Enter request ID: ")
                print(manager.view(request_id))

            elif choice == "3":
                request_id = input("Enter request ID: ")
                approver = input("Enter approver name: ")
                print(manager.approve(request_id, approver))

            elif choice == "4":
                request_id = input("Enter request ID: ")
                print(manager.issue(request_id))

            elif choice == "5":
                request_id = input("Enter request ID: ")
                print(manager.return_card(request_id))

            elif choice == "6":
                requests = manager.list()

                if requests:
                    for request in requests:
                        print(request)
                else:
                    print("No requests found.")

            elif choice == "7":
                save_manager(manager, DATA_FILE)
                print("Requests saved successfully.")

            elif choice == "8":
                manager = load_manager(DATA_FILE)
                print("Requests reloaded successfully.")

            elif choice == "9":
                print("Goodbye!")
                break

            else:
                print("Invalid option. Choose 1–9.")

        except (RequestError, DataError) as error:
            print("Error:", error)


if __name__ == "__main__":
    run()