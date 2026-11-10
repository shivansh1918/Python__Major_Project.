
class Complaint:

    def __init__(self, database):

        self.database = database

        self.categories = [
            "Electricity",
            "Transport",
            "Water Supply",
            "Classroom",
            "Washroom",
            "Library",
            "Computer Lab",
            "Cleanliness",
            "Other"
        ]

    # Submit a new complaint
    def submit_complaint(self, student_id):

        print("\n========== SUBMIT COMPLAINT ==========")

        print("\nSelect Complaint Category:")

        for index, category in enumerate(self.categories, start=1):

            print(f"{index}. {category}")

        try:

            choice = int(input("\nEnter Category Number: "))

            if choice < 1 or choice > len(self.categories):

                print("Invalid Category Selection.")
                return

        except ValueError:

            print("Please enter a valid number.")
            return

        title = self.categories[choice - 1]

        if title == "Other":

            title = input("Enter Complaint Title: ").strip()

            if not title:

                print("Complaint title cannot be empty.")
                return

        description = input(
            "Complaint Description: "
        ).strip()

        if not description:

            print("Complaint description cannot be empty.")
            return

        result = self.database.create_complaint(
            student_id,
            title,
            description
        )

        if result is not None and result > 0:

            print("\nComplaint Submitted Successfully!")
            print("Complaint Category:", title)
            print("Current Status: Pending")

        else:

            print("\nComplaint could not be submitted.")

    # Display complaints
    def view_complaints(self, student_id=None, status=None):

        complaints = self.database.get_complaints(
            student_id,
            status
        )

        if complaints is None:

            print("Unable to retrieve complaints.")
            return

        if not complaints:

            print("\nNo complaints found.")
            return

        print("\n========== COMPLAINT LIST ==========")

        for item in complaints:

            print("\nComplaint ID:", item["complaint_id"])

            print("Student ID:", item["student_id"])

            print("Student Name:", item["name"])

            print("Title:", item["complaint_title"])

            print(
                "Description:",
                item["complaint_description"]
            )

            print("Status:", item["status"])

            note = item.get("admin_note")

            if note:

                print("Admin Note:", note)

            else:

                print("Admin Note: No note added yet.")

            print("Created At:", item["created_at"])

            print("Updated At:", item["updated_at"])

            print("-" * 40)