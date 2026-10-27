from getpass import getpass
from security import Security
from complaint import Complaint


class Student:

    def __init__(self, database):
        self.database = database
        self.complaint = Complaint(database)

    # Student registration
    def register(self):

        print("\n========== STUDENT REGISTRATION ==========")

        name = input("Full Name: ").strip()
        student_id = input("Student ID: ").strip()
        course = input("Course: ").strip()

        if not name or not student_id or not course:
            print("All fields are required.")
            return

        # Validate course year
        try:
            course_year = int(input("Course Year: "))

            if course_year < 1 or course_year > 6:
                print("Course Year must be between 1 and 6.")
                return

        except ValueError:
            print("Course Year must be a number.")
            return

        # Check duplicate Student ID
        existing_student = self.database.get_student(student_id)

        if existing_student is not None:
            print("Student ID already registered.")
            return

        password = getpass("Create Password: ")
        confirm_password = getpass("Confirm Password: ")

        if not password:
            print("Password cannot be empty.")
            return

        if password != confirm_password:
            print("Passwords do not match.")
            return

        password_hash = Security.hash_password(password)

        result = self.database.create_student(
            student_id,
            name,
            password_hash,
            course,
            course_year
        )

        if result is not None and result > 0:
            print("\nRegistration Successful!")
        else:
            print("\nRegistration Failed.")

    # Student login
    def login(self):

        print("\n========== STUDENT LOGIN ==========")

        student_id = input("Student ID: ").strip()
        password = getpass("Password: ")

        if not student_id or not password:
            print("Student ID and Password are required.")
            return

        student = self.database.get_student(student_id)

        if student is None:
            print("Invalid Student ID or Password.")
            return

        if not Security.verify_password(
            password,
            student["password_hash"]
        ):
            print("Invalid Student ID or Password.")
            return

        print("\nLogin Successful!")
        print("Welcome,", student["name"])

        self.dashboard(student)

    # Student dashboard
    def dashboard(self, student):

        while True:

            print("\n========== STUDENT DASHBOARD ==========")
            print("1. Submit Complaint")
            print("2. View My Complaints")
            print("3. Logout")

            choice = input("Enter Choice: ").strip()

            if choice == "1":

                self.complaint.submit_complaint(
                    student["student_id"]
                )

            elif choice == "2":

                self.complaint.view_complaints(
                    student_id=student["student_id"]
                )

            elif choice == "3":

                print("Student Logged Out Successfully.")
                break

            else:
                print("Invalid Choice. Please Try Again.")