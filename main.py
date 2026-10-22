import sqlite3
from pathlib import Path

# Keep the database in the same folder as this program.
database_path = Path(__file__).resolve().parent / "applications.db"
connection = sqlite3.connect(database_path)

# Create the table if it does not already exist.
connection.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY,
        company TEXT NOT NULL,
        position TEXT NOT NULL,
        status TEXT NOT NULL
    )
""")

while True:
    print("\nInternship Application Tracker")
    print("1. Add an application")
    print("2. View applications")
    print("3. Update application status")
    print("4. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        company = input("Company name: ").strip()
        position = input("Position title: ").strip()

        if not company or not position:
            print("Company and position cannot be empty.")
            continue

        with connection:
            connection.execute(
                """
                INSERT INTO applications (company, position, status)
                VALUES (?, ?, ?)
                """,
                (company, position, "Interested")
            )

        print("Application saved!")

    elif choice == "2":
        applications = connection.execute(
            """
            SELECT id, company, position, status
            FROM applications
            ORDER BY id
            """
        ).fetchall()

        if not applications:
            print("No applications recorded yet. Choose option 1 to add one.")
        else:
            print("\nSaved applications:")

            for application_id, company, position, status in applications:
                print(f"\nApplication ID: {application_id}")
                print(f"Company: {company}")
                print(f"Position: {position}")
                print(f"Status: {status}")

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

        print(f"\nUpdating: {application[0]} | {application[1]}")

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

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid option. Please enter 1, 2, 3, or 4.")

connection.close()