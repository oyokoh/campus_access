import unittest

from campus_access.errors import RequestError
from campus_access.work import RequestManager


class AdditionalRequestCases(unittest.TestCase):
    def setUp(self):
        self.manager = RequestManager()

    def test_failed_creation_does_not_consume_id(self):
        with self.assertRaises(RequestError):
            self.manager.create("F001", "visitor-card")
        request = self.manager.create("F001", "visitor")
        self.assertEqual(request["id"], "A001")

    def test_approval_cannot_be_repeated(self):
        request = self.manager.create("F001", "visitor")
        self.manager.approve(request["id"], "Staff One")
        with self.assertRaises(RequestError):
            self.manager.approve(request["id"], "Staff Two")
        self.assertEqual(self.manager.view(request["id"])["approved_by"], "Staff One")

    def test_issue_cannot_be_repeated(self):
        request = self.manager.create("F001", "student")
        self.manager.approve(request["id"], "Staff One")
        self.manager.issue(request["id"])
        with self.assertRaises(RequestError):
            self.manager.issue(request["id"])
        self.assertEqual(self.manager.view(request["id"])["status"], "issued")

    def test_returned_request_cannot_be_issued_again(self):
        request = self.manager.create("F001", "staff")
        self.manager.approve(request["id"], "Staff One")
        self.manager.issue(request["id"])
        self.manager.return_card(request["id"])
        with self.assertRaises(RequestError):
            self.manager.issue(request["id"])
        self.assertEqual(self.manager.view(request["id"])["status"], "returned")

    def test_card_type_is_case_sensitive(self):
        with self.assertRaises(RequestError):
            self.manager.create("F001", "Visitor")

    def test_status_filter_returns_only_matching_requests(self):
        first = self.manager.create("F001", "visitor")
        second = self.manager.create("F002", "student")
        self.manager.approve(second["id"], "Staff One")
        self.assertEqual(self.manager.list("requested"), [first])
        self.assertEqual(self.manager.list("approved"), [self.manager.view(second["id"])])

    def test_duplicate_ids_in_saved_data_are_rejected(self):
        manager = RequestManager()
        record = manager.create("F001", "visitor")
        data = manager.to_dict()
        data["requests"].append(dict(record))
        with self.assertRaises(RequestError):
            RequestManager.from_dict(data)

    def test_saved_requested_record_cannot_have_approver(self):
        manager = RequestManager()
        manager.create("F001", "visitor")
        data = manager.to_dict()
        data["requests"][0]["approved_by"] = "Staff One"
        with self.assertRaises(RequestError):
            RequestManager.from_dict(data)


if __name__ == "__main__":
    unittest.main()
