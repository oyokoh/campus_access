import unittest

from campus_access.work import RequestManager
from campus_access.errors import RequestError


class TestRequestManager(unittest.TestCase):

    def setUp(self):
        self.manager = RequestManager()

    def test_create_valid_request(self):
        request = self.manager.create("F001", "visitor")

        self.assertEqual(request["id"], "A001")
        self.assertEqual(request["fellow_id"], "F001")
        self.assertEqual(request["card_type"], "visitor")
        self.assertEqual(request["status"], "requested")
        self.assertIsNone(request["approved_by"])

    def test_blank_fellow_id_is_rejected(self):
        with self.assertRaises(RequestError):
            self.manager.create("", "visitor")

    def test_whitespace_fellow_id_is_rejected(self):
        with self.assertRaises(RequestError):
            self.manager.create("   ", "visitor")

    def test_non_string_fellow_id_is_rejected(self):
        with self.assertRaises(RequestError):
            self.manager.create(123, "visitor")

    def test_invalid_card_type_is_rejected(self):
        with self.assertRaises(RequestError):
            self.manager.create("F001", "invalid")

    def test_non_string_card_type_is_rejected(self):
        with self.assertRaises(RequestError):
            self.manager.create("F001", 123)

    def test_malformed_id_is_rejected(self):
        self.manager.create("F001", "visitor")

        for request_id in ("A", "A00", "A000", "A-01", "A１２３"):
            with self.subTest(request_id=request_id):
                with self.assertRaises(RequestError):
                    self.manager.view(request_id)

    def test_unknown_id_is_rejected(self):
        with self.assertRaises(RequestError):
            self.manager.view("A999")

    def test_view_returns_a_copy(self):
        self.manager.create("F001", "visitor")

        request = self.manager.view("A001")
        request["status"] = "returned"

        self.assertEqual(
            self.manager.view("A001")["status"],
            "requested",
        )

    def test_issue_before_approval_is_rejected(self):
        self.manager.create("F001", "visitor")
        before = self.manager.view("A001")

        with self.assertRaises(RequestError):
            self.manager.issue("A001")

        self.assertEqual(self.manager.view("A001"), before)

    def test_blank_approver_is_rejected(self):
        self.manager.create("F001", "visitor")
        before = self.manager.view("A001")

        with self.assertRaises(RequestError):
            self.manager.approve("A001", "   ")

        self.assertEqual(self.manager.view("A001"), before)

    def test_complete_workflow(self):
        self.manager.create("F001", "visitor")

        self.manager.approve("A001", "M01")
        self.assertEqual(
            self.manager.view("A001")["status"],
            "approved",
        )

        self.manager.issue("A001")
        self.assertEqual(
            self.manager.view("A001")["status"],
            "issued",
        )

        self.manager.return_card("A001")
        request = self.manager.view("A001")

        self.assertEqual(request["status"], "returned")
        self.assertEqual(request["approved_by"], "M01")

    def test_returning_twice_is_rejected(self):
        self.manager.create("F001", "visitor")
        self.manager.approve("A001", "M01")
        self.manager.issue("A001")
        self.manager.return_card("A001")

        before = self.manager.view("A001")

        with self.assertRaises(RequestError):
            self.manager.return_card("A001")

        self.assertEqual(self.manager.view("A001"), before)

    def test_ids_are_unique(self):
        first = self.manager.create("F001", "visitor")
        second = self.manager.create("F002", "student")

        self.assertEqual(first["id"], "A001")
        self.assertEqual(second["id"], "A002")
        self.assertNotEqual(first["id"], second["id"])

    def test_to_dict_contains_requests_and_next_id(self):
        self.manager.create("F001", "visitor")

        data = self.manager.to_dict()

        self.assertIn("requests", data)
        self.assertIn("next_id", data)
        self.assertEqual(data["next_id"], 2)
        self.assertEqual(len(data["requests"]), 1)


if __name__ == "__main__":
    unittest.main()