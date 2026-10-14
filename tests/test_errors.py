import unittest

from campus_access.errors import RequestError, DataError


class TestErrors(unittest.TestCase):

    def test_request_error_is_exception(self):
        self.assertTrue(issubclass(RequestError, Exception))

    def test_data_error_is_exception(self):
        self.assertTrue(issubclass(DataError, Exception))

    def test_request_error_message(self):
        error = RequestError("Invalid request")
        self.assertEqual(str(error), "Invalid request")

    def test_data_error_message(self):
        error = DataError("Invalid saved data")
        self.assertEqual(str(error), "Invalid saved data")


if __name__ == "__main__":
    unittest.main()