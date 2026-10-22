import io
import sqlite3
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main


class TrackerTests(unittest.TestCase):

    def setUp(self):
        # Give each test its own temporary database.
        self.temp_directory = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_directory.name) / "test.db"

        self.connection = self.open_database()
        main.initialize_database(self.connection)

    def tearDown(self):
        self.connection.close()
        self.temp_directory.cleanup()

    def open_database(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def run_action(self, action, answers):
        # Supply simulated keyboard input and hide menu output.
        with patch("builtins.input", side_effect=answers):
            with redirect_stdout(io.StringIO()):
                action(self.connection)

    def add_sample(self):
        with self.connection:
            cursor = self.connection.execute(
                """
                INSERT INTO applications (
                    company, position, status, posting_url, deadline
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    "Example Company",
                    "Software Intern",
                    "Interested",
                    "https://example.com/job",
                    "2027-03-01"
                )
            )

        return cursor.lastrowid

    def test_add_rejects_invalid_deadline(self):
        self.run_action(
            main.add_application,
            [
                "Test Company",
                "Software Intern",
                "https://example.com/job",
                "2027-02-30",
                "2027-03-01"
            ]
        )

        applications = self.connection.execute(
            "SELECT * FROM applications"
        ).fetchall()

        self.assertEqual(len(applications), 1)
        self.assertEqual(applications[0]["company"], "Test Company")
        self.assertEqual(applications[0]["status"], "Interested")
        self.assertEqual(applications[0]["deadline"], "2027-03-01")

    def test_data_survives_database_reopening(self):
        self.run_action(
            main.add_application,
            ["Test Company", "Software Intern", "", ""]
        )

        self.connection.close()
        self.connection = self.open_database()
        main.initialize_database(self.connection)

        application = self.connection.execute(
            "SELECT * FROM applications"
        ).fetchone()

        self.assertIsNotNone(application)
        self.assertEqual(application["company"], "Test Company")

    def test_status_validation_and_update(self):
        application_id = self.add_sample()

        self.run_action(
            main.update_status,
            [str(application_id), "invalid"]
        )

        application = self.connection.execute(
            "SELECT * FROM applications WHERE id = ?",
            (application_id,)
        ).fetchone()

        self.assertEqual(application["status"], "Interested")

        self.run_action(
            main.update_status,
            [str(application_id), "2"]
        )

        application = self.connection.execute(
            "SELECT * FROM applications WHERE id = ?",
            (application_id,)
        ).fetchone()

        self.assertEqual(application["status"], "Applied")

    def test_edit_keeps_blank_fields_and_clears_link(self):
        application_id = self.add_sample()

        self.run_action(
            main.edit_application,
            [str(application_id), "Updated Company", "", "-", ""]
        )

        application = self.connection.execute(
            "SELECT * FROM applications WHERE id = ?",
            (application_id,)
        ).fetchone()

        self.assertEqual(application["company"], "Updated Company")
        self.assertEqual(application["position"], "Software Intern")
        self.assertEqual(application["posting_url"], "")
        self.assertEqual(application["deadline"], "2027-03-01")
        self.assertEqual(application["status"], "Interested")

    def test_cancelled_deletion_keeps_record(self):
        application_id = self.add_sample()

        self.run_action(
            main.delete_application,
            [str(application_id), "no"]
        )

        count = self.connection.execute(
            "SELECT COUNT(*) FROM applications"
        ).fetchone()[0]

        self.assertEqual(count, 1)

    def test_confirmed_deletion_removes_record(self):
        application_id = self.add_sample()

        self.run_action(
            main.delete_application,
            [str(application_id), "yes"]
        )

        count = self.connection.execute(
            "SELECT COUNT(*) FROM applications"
        ).fetchone()[0]

        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()