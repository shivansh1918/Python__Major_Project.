from database import Database
from student import Student
from admin import Admin


def main():

    database = Database()

    student = Student(database)
    admin = Admin(database)

    print("\n==========================================")
    print("    STUDENT COMPLAINT MANAGEMENT SYSTEM")
    print("==========================================")

    while True:

        admin_exists = database.admin_exists()

        if admin_exists is None:
            print("\nDatabase connection failed.")
            print("Please check database.py settings.")
            break

        print("\n============== MAIN MENU ==============")
        print("1. Student Registration")
        print("2. Student Login")

        if not admin_exists:
            print("3. Admin Setup")
            print("4. Exit")

        else:
            print("3. Admin Login")
            print("4. Exit")

        choice = input("Enter Your Choice: ").strip()

        if choice == "1":

            student.register()

        elif choice == "2":

            student.login()

        elif choice == "3":

            if not admin_exists:
                admin.setup_admin()
            else:
                admin.login()

        elif choice == "4":

            print("\nThank You for Using the System!")
            break

        else:
            print("Invalid Choice. Please Try Again.")


if __name__ == "__main__":
    main()
    
    # admin -pass 12345678, student-MCA2026081 pass- 12345678
    
    