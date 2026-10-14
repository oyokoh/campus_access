"""Tests for saving and loading campus access-card requests."""

import json
import os
import tempfile
import unittest

from campus_access.errors import DataError
from campus_access.storage import save_manager, load_manager
from campus_access.work import RequestManager


class TestStorage(unittest.TestCase):

    def setUp(self):
        """Create a temporary folder for each test."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.path = os.path.join(
            self.temp_dir.name,
            "cards.json",
        )

        self.manager = RequestManager()

    # Tests for saving requests

    def test_save_creates_json_file(self):
        self.manager.create("F001", "visitor")

        save_manager(self.manager, self.path)

        self.assertTrue(os.path.isfile(self.path))

    def test_saved_json_contains_request_fields(self):
        self.manager.create("F001", "visitor")

        save_manager(self.manager, self.path)

        with open(self.path, encoding="utf-8") as file:
            data = json.load(file)

        request = data["requests"][0]

        self.assertEqual(request["id"], "A001")
        self.assertEqual(request["fellow_id"], "F001")
        self.assertEqual(request["card_type"], "visitor")
        self.assertEqual(request["status"], "requested")
        self.assertIsNone(request["approved_by"])

    def test_save_preserves_next_id(self):
        self.manager.create("F001", "visitor")
        self.manager.create("F002", "student")

        save_manager(self.manager, self.path)

        with open(self.path, encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(data["next_id"], 3)

    def test_save_replaces_existing_file(self):
        with open(self.path, "w", encoding="utf-8") as file:
            file.write("old content")

        self.manager.create("F001", "visitor")
        save_manager(self.manager, self.path)

        with open(self.path, encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(data["requests"][0]["id"], "A001")

    def test_save_failure_raises_data_error(self):
        invalid_path = os.path.join(
            self.temp_dir.name,
            "missing",
            "cards.json",
        )

        with self.assertRaises(DataError):
            save_manager(self.manager, invalid_path)

    # Tests for loading requests

    def test_load_restores_saved_requests(self):
        self.manager.create("F001", "visitor")
        save_manager(self.manager, self.path)

        loaded_manager = load_manager(self.path)

        request = loaded_manager.view("A001")

        self.assertEqual(request["fellow_id"], "F001")
        self.assertEqual(request["card_type"], "visitor")
        self.assertEqual(request["status"], "requested")
        self.assertIsNone(request["approved_by"])

    def test_load_preserves_next_id(self):
        self.manager.create("F001", "visitor")
        self.manager.create("F002", "student")

        save_manager(self.manager, self.path)

        loaded_manager = load_manager(self.path)
        new_request = loaded_manager.create("F003", "staff")

        self.assertEqual(new_request["id"], "A003")

    def test_load_invalid_json_raises_data_error(self):
        with open(self.path, "w", encoding="utf-8") as file:
            file.write("{invalid json")

        with self.assertRaises(DataError):
            load_manager(self.path)

    def test_load_invalid_data_raises_data_error(self):
        invalid_data = {
            "requests": [
                {
                    "id": "A001",
                    "fellow_id": "",
                    "card_type": "visitor",
                    "status": "requested",
                    "approved_by": None,
                }
            ],
            "next_id": 2,
        }

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(invalid_data, file)

        with self.assertRaises(DataError):
            load_manager(self.path)


if __name__ == "__main__":
    unittest.main()