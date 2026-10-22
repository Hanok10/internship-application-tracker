# internship-application-tracker

A Python command-line application for organizing internship applications.
It stores records locally in a SQLite database so they remain available
after the program closes.

## Features

- Add applications with a company name and position title.
- Store optional posting links and application deadlines.
- View saved applications with clearly labeled IDs.
- Update statuses: Interested, Applied, Interviewing, Offer, Rejected,
  or Withdrawn.
- Edit application details.
- Delete applications after confirmation.
- Validate required fields, application IDs, and deadline dates.
- Upgrade older database tables when new fields are introduced.

## Technologies

- Python
- SQLite through Python's built-in `sqlite3` module
- `pathlib` for locating the database file
- `datetime` for validating dates
- Git and GitHub for version control

## Requirements

- Python 3.9 or later
- Git, if cloning the repository

No additional Python packages are required.

## Getting Started

Clone the repository:

```bash
git clone https://github.com/Hanok10/internship-application-tracker.git
```

Open the project directory:

```bash
cd internship-application-tracker
```

Run the program:

```bash
python3 main.py
```

## Usage

Choose an option from the menu:

```text
Internship Application Tracker
1. Add an application
2. View applications
3. Update application status
4. Delete an application
5. Edit application details
6. Exit
```

New applications start with the status `Interested`.

Use the displayed Application ID when updating, editing, or deleting
a record. The ID is separate from the menu option number.

Enter deadlines in `YYYY-MM-DD` format. Leave the deadline blank
if it is unknown.

When editing:
- Press Enter to keep an existing value.
- Enter `-` to clear a posting link or deadline.

## Data Storage

The program automatically creates `applications.db` in the same directory
as `main.py`.

Application records are stored in this local database. The database is
excluded from version control through `.gitignore`.

## Learning Focus

This project demonstrates:

- Organizing a program into reusable functions
- Creating, reading, updating, and deleting database records
- Using parameterized SQL queries
- Validating user input and handling invalid values
- Preserving data between program runs
- Maintaining compatibility with an existing database