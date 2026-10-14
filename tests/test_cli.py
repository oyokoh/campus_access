import unittest
from unittest.mock import patch
from io import StringIO

from campus_access.cli import run


class TestCLI(unittest.TestCase):

    @patch("builtins.input", side_effect=["4"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_exit_menu(self, mock_output, mock_input):
        run()
        self.assertIn("Goodbye!", mock_output.getvalue())

    @patch("builtins.input", side_effect=["invalid", "4"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_option(self, mock_output, mock_input):
        run()
        self.assertIn("Invalid option", mock_output.getvalue())

    @patch("builtins.input", side_effect=["1", "F001", "visitor", "4"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_create_request(self, mock_output, mock_input):
        run()
        self.assertIn("A001", mock_output.getvalue())
        self.assertIn("Request created", mock_output.getvalue())

    @patch("builtins.input", side_effect=["1", "", "visitor", "4"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_blank_fellow_id(self, mock_output, mock_input):
        run()
        self.assertIn("Error:", mock_output.getvalue())

    @patch("builtins.input", side_effect=["1", "F001", "invalid", "4"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_card_type(self, mock_output, mock_input):
        run()
        self.assertIn("Error:", mock_output.getvalue())

    @patch("builtins.input", side_effect=["1", "F001", "visitor", "2", "A001", "4"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_view_request(self, mock_output, mock_input):
        run()
        self.assertIn("A001", mock_output.getvalue())
        self.assertIn("F001", mock_output.getvalue())

    @patch("builtins.input", side_effect=["3", "4"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_list_empty_requests(self, mock_output, mock_input):
        run()
        self.assertIn("No requests found", mock_output.getvalue())


if __name__ == "__main__":
    unittest.main()