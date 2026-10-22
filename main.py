import sqlite3
from pathlib import Path

database_path = Path(__file__).resolve().parent / "applications.db"
connection = sqlite3.connect(database_path)

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
    print("3. Exit")

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
            print("No applications recorded yet.")
        else:
            for application_id, company, position, status in applications:
                print(
                    f"{application_id}. {company} | "
                    f"{position} | {status}"
                )

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid option. Please enter 1, 2, or 3.")

connection.close()