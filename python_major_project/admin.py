from getpass import getpass
from security import Security
from complaint import Complaint


class Admin:

    def __init__(self, database):
        self.database = database
        self.complaint = Complaint(database)

    # First-time admin setup
    def setup_admin(self):

        exists = self.database.admin_exists()

        if exists is None:
            print("Unable to check admin account.")
            return

        if exists:
            print("Admin account already exists.")
            print("Please use Admin Login.")
            return

        print("\n========== ADMIN SETUP ==========")

        username = input("Create Admin Username: ").strip()

        if not username:
            print("Username cannot be empty.")
            return

        password = getpass("Create Admin Password: ")
        confirm_password = getpass("Confirm Admin Password: ")

        if not password:
            print("Password cannot be empty.")
            return

        if password != confirm_password:
            print("Passwords do not match.")
            return

        password_hash = Security.hash_password(password)

        result = self.database.create_admin(
            username,
            password_hash
        )

        if result is not None and result > 0:
            print("\nAdmin Account Created Successfully!")
        else:
            print("\nAdmin Setup Failed.")

    # Admin login
    def login(self):

        exists = self.database.admin_exists()

        if exists is None:
            print("Unable to check admin account.")
            return

        if not exists:
            print("No Admin Account Found.")
            print("Please Complete Admin Setup First.")
            return

        print("\n========== ADMIN LOGIN ==========")

        username = input("Admin Username: ").strip()
        password = getpass("Admin Password: ")

        if not username or not password:
            print("Username and Password are required.")
            return

        admin = self.database.get_admin(username)

        if admin is None:
            print("Invalid Username or Password.")
            return

        if not Security.verify_password(
            password,
            admin["password_hash"]
        ):
            print("Invalid Username or Password.")
            return

        print("\nAdmin Login Successful!")

        self.dashboard()

    # Display all students
    def view_students(self):

        students = self.database.get_all_students()

        if students is None:
            print("Unable to retrieve students.")
            return

        if not students:
            print("No Students Registered Yet.")
            return

        print("\n========== REGISTERED STUDENTS ==========")

        for student in students:

            print("\nStudent ID:", student["student_id"])
            print("Name:", student["name"])
            print("Course:", student["course"])
            print("Course Year:", student["course_year"])
            print("Registered At:", student["created_at"])
            print("-" * 40)

    # Update complaint status
    def update_status(self):

        print("\n========== UPDATE COMPLAINT STATUS ==========")

        try:
            complaint_id = int(input("Enter Complaint ID: "))

            if complaint_id <= 0:
                print("Complaint ID must be positive.")
                return

        except ValueError:
            print("Complaint ID must be a number.")
            return

        print("\n1. Pending")
        print("2. In Progress")
        print("3. Solved")

        choice = input("Select New Status: ").strip()

        status_options = {
            "1": "Pending",
            "2": "In Progress",
            "3": "Solved"
        }

        status = status_options.get(choice)

        if status is None:
            print("Invalid Status Selection.")
            return

        # Check whether complaint exists
        complaints = self.database.get_complaints()

        if complaints is None:
            print("Unable to retrieve complaints.")
            return

        if not any(
            item["complaint_id"] == complaint_id
            for item in complaints
        ):
            print("Complaint ID Not Found.")
            return

        result = self.database.update_complaint_status(
            complaint_id,
            status
        )

        if result is not None and result > 0:
            print("Complaint Status Updated Successfully!")
        elif result == 0:
            print("Complaint Status Was Not Changed.")
        else:
            print("Failed to Update Complaint Status.")

    # Admin dashboard
    def dashboard(self):

        while True:

            print("\n========== ADMIN DASHBOARD ==========")
            print("1. View All Students")
            print("2. View All Complaints")
            print("3. View Pending Complaints")
            print("4. View In Progress Complaints")
            print("5. View Solved Complaints")
            print("6. Update Complaint Status")
            print("7. Logout")

            choice = input("Enter Choice: ").strip()

            if choice == "1":

                self.view_students()

            elif choice == "2":

                self.complaint.view_complaints()

            elif choice == "3":

                self.complaint.view_complaints(
                    status="Pending"
                )

            elif choice == "4":

                self.complaint.view_complaints(
                    status="In Progress"
                )

            elif choice == "5":

                self.complaint.view_complaints(
                    status="Solved"
                )

            elif choice == "6":

                self.update_status()

            elif choice == "7":

                print("Admin Logged Out Successfully.")
                break

            else:
                print("Invalid Choice. Please Try Again.")