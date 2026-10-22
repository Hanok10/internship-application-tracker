import sqlite3
from datetime import date
from pathlib import Path

# Keep the database beside this program.
database_path = Path(__file__).resolve().parent / "applications.db"
connection = sqlite3.connect(database_path)

# Create the original table if needed.
connection.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY,
        company TEXT NOT NULL,
        position TEXT NOT NULL,
        status TEXT NOT NULL
    )
""")

# Check which columns already exist.
columns = {
    column[1]
    for column in connection.execute("PRAGMA table_info(applications)")
}

# Add the new columns to existing databases.
with connection:
    if "posting_url" not in columns:
        connection.execute("""
            ALTER TABLE applications
            ADD COLUMN posting_url TEXT NOT NULL DEFAULT ''
        """)

    if "deadline" not in columns:
        connection.execute("""
            ALTER TABLE applications
            ADD COLUMN deadline TEXT NOT NULL DEFAULT ''
        """)

while True:
    print("\nInternship Application Tracker")
    print("1. Add an application")
    print("2. View applications")
    print("3. Update application status")
    print("4. Delete an application")
    print("5. Exit")

    choice = input("Choose an option: ").strip()

    # Add a new application.
    if choice == "1":
        company = input("Company name: ").strip()
        position = input("Position title: ").strip()

        if not company or not position:
            print("Company and position cannot be empty.")
            continue

        posting_url = input(
            "Posting link (press Enter to skip): "
        ).strip()

        while True:
            deadline = input(
                "Deadline YYYY-MM-DD (press Enter if unknown): "
            ).strip()

            if not deadline:
                break

            try:
                date.fromisoformat(deadline)
                break
            except ValueError:
                print("Enter a valid date, such as 2026-11-20.")

        with connection:
            cursor = connection.execute(
                """
                INSERT INTO applications (
                    company, position, status, posting_url, deadline
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (company, position, "Interested", posting_url, deadline)
            )

        print(f"Application saved! Application ID: {cursor.lastrowid}")

    # Display all saved applications.
    elif choice == "2":
        applications = connection.execute(
            """
            SELECT id, company, position, status, posting_url, deadline
            FROM applications
            ORDER BY id
            """
        ).fetchall()

        if not applications:
            print("No applications recorded yet. Choose option 1 to add one.")
        else:
            print("\nSaved applications:")

            for application in applications:
                (
                    application_id,
                    company,
                    position,
                    status,
                    posting_url,
                    deadline
                ) = application

                print(f"\nApplication ID: {application_id}")
                print(f"Company: {company}")
                print(f"Position: {position}")
                print(f"Status: {status}")
                print(f"Posting link: {posting_url or 'Not provided'}")
                print(f"Deadline: {deadline or 'Unknown'}")

    # Update an application's status.
    elif choice == "3":
        try:
            application_id = int(input("Application ID to update: "))
        except ValueError:
            print("Please enter a whole number.")
            continue

        application = connection.execute(
            "SELECT company, position FROM applications WHERE id = ?",
            (application_id,)
        ).fetchone()

        if application is None:
            print("No application found with that ID.")
            continue

        print(f"\nCompany: {application[0]}")
        print(f"Position: {application[1]}")

        statuses = {
            "1": "Interested",
            "2": "Applied",
            "3": "Interviewing",
            "4": "Offer",
            "5": "Rejected",
            "6": "Withdrawn"
        }

        for number, status in statuses.items():
            print(f"{number}. {status}")

        status_choice = input("Choose the new status: ").strip()

        if status_choice not in statuses:
            print("Invalid status selection.")
            continue

        with connection:
            connection.execute(
                "UPDATE applications SET status = ? WHERE id = ?",
                (statuses[status_choice], application_id)
            )

        print("Status updated!")

    # Delete an application after confirmation.
    elif choice == "4":
        try:
            application_id = int(input("Application ID to delete: "))
        except ValueError:
            print("Please enter a whole number.")
            continue

        application = connection.execute(
            "SELECT company, position FROM applications WHERE id = ?",
            (application_id,)
        ).fetchone()

        if application is None:
            print("No application found with that ID.")
            continue

        print(f"\nCompany: {application[0]}")
        print(f"Position: {application[1]}")

        confirmation = input(
            "Type yes to permanently delete this application: "
        ).strip().lower()

        if confirmation != "yes":
            print("Deletion cancelled.")
            continue

        with connection:
            connection.execute(
                "DELETE FROM applications WHERE id = ?",
                (application_id,)
            )

        print("Application deleted.")

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid option. Please enter 1, 2, 3, 4, or 5.")

connection.close()