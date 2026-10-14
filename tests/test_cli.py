"""Tests for the campus access-card command-line interface."""

import unittest
from unittest.mock import patch
from io import StringIO

from campus_access.cli import run


class TestCLI(unittest.TestCase):

    @patch("builtins.input", side_effect=["9"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_exit_menu(self, mock_output, mock_input):
        run()
        self.assertIn("Goodbye!", mock_output.getvalue())

    @patch("builtins.input", side_effect=["invalid", "9"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_option(self, mock_output, mock_input):
        run()
        self.assertIn("Invalid option", mock_output.getvalue())

    @patch("builtins.input", side_effect=["1", "F001", "visitor", "9"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_create_request(self, mock_output, mock_input):
        run()
        output = mock_output.getvalue()
        self.assertIn("A001", output)
        self.assertIn("Request created", output)

    @patch("builtins.input", side_effect=["1", "", "visitor", "9"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_blank_fellow_id(self, mock_output, mock_input):
        run()
        self.assertIn("Error:", mock_output.getvalue())

    @patch("builtins.input", side_effect=["1", "F001", "invalid", "9"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_card_type(self, mock_output, mock_input):
        run()
        self.assertIn("Error:", mock_output.getvalue())

    @patch(
        "builtins.input",
        side_effect=["1", "F001", "visitor", "2", "A001", "9"],
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_view_request(self, mock_output, mock_input):
        run()
        output = mock_output.getvalue()
        self.assertIn("A001", output)
        self.assertIn("F001", output)

    @patch("builtins.input", side_effect=["6", "9"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_list_empty_requests(self, mock_output, mock_input):
        run()
        self.assertIn("No requests found", mock_output.getvalue())

    @patch(
        "builtins.input",
        side_effect=[
            "1", "F001", "visitor",
            "3", "A001", "Manager",
            "4", "A001",
            "5", "A001",
            "2", "A001",
            "9",
        ],
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_complete_workflow(self, mock_output, mock_input):
        run()
        output = mock_output.getvalue()
        self.assertIn("approved", output)
        self.assertIn("issued", output)
        self.assertIn("returned", output)

    @patch("builtins.input", side_effect=["2", "A999", "9"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_view_unknown_request(self, mock_output, mock_input):
        run()
        self.assertIn("Error:", mock_output.getvalue())


if __name__ == "__main__":
    unittest.main()