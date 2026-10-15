
"""Save and load campus access-card requests."""

import json
import os
import tempfile

from campus_access.errors import DataError, RequestError
from campus_access.work import RequestManager


def save_manager(manager, path):
    """Save requests to a JSON file safely."""
    temporary_path = None

    try:
        data = manager.to_dict()
        path = os.path.abspath(path)
        directory = os.path.dirname(path)

        os.makedirs(directory, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=directory,
            delete=False
        ) as file:
            temporary_path = file.name
            json.dump(data, file, indent=4)
            file.write("\n")

        os.replace(temporary_path, path)
        temporary_path = None

    except (OSError, TypeError, ValueError) as error:
        raise DataError("Could not save requests: %s" % error) from error

    finally:
        if temporary_path is not None:
            try:
                os.unlink(temporary_path)
            except OSError:
                pass


def load_manager(path):
    """Load and validate requests from a JSON file."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return RequestManager.from_dict(data)

    except FileNotFoundError as error:
        raise DataError("Saved requests file was not found.") from error

    except json.JSONDecodeError as error:
        raise DataError("Saved requests file contains invalid JSON.") from error

    except UnicodeDecodeError as error:
        raise DataError("Saved requests file is not valid UTF-8.") from error

    except OSError as error:
        raise DataError("Could not read requests: %s" % error) from error

    except RequestError as error:
        raise DataError("Saved requests are invalid: %s" % error) from error