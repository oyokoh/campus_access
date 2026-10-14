from campus_access.work import RequestManager
from campus_access.errors import RequestError


def run():
    manager = RequestManager()

    while True:
        print("\nCampus Access-Card Manager")
        print("1. Create request")
        print("2. View request")
        print("3. List requests")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                fellow_id = input("Enter fellow ID: ")
                card_type = input("Enter card type (visitor/student/staff): ")

                request = manager.create(fellow_id, card_type)
                print("Request created:", request)

            elif choice == "2":
                request_id = input("Enter request ID: ")
                print(manager.view(request_id))

            elif choice == "3":
                requests = manager.list()

                if requests:
                    for request in requests:
                        print(request)
                else:
                    print("No requests found.")

            elif choice == "4":
                print("Goodbye!")
                break

            else:
                print("Invalid option. Please choose 1, 2, 3, or 4.")

        except RequestError as error:
            print("Error:", error)