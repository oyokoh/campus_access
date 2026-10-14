import json
import os
import tempfile

from campus_access.errors import DataError
from campus_access.work import RequestManager


def save_manager(manager, path):
    """Save the request manager's data to a JSON file."""
    data = manager.to_dict()
    directory = os.path.dirname(os.path.abspath(path))

    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=directory,
            delete=False,
        ) as file:
            temporary_path = file.name
            json.dump(data, file, indent=4)
            file.write("\n")

        os.replace(temporary_path, path)

    except (OSError, TypeError, ValueError) as error:
        raise DataError("Could not save requests: %s" % error) from error

    finally:
        if temporary_path is not None and os.path.exists(temporary_path):
            os.unlink(temporary_path)