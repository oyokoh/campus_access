
"""Core workflow for the campus access-card request manager."""

from campus_access.errors import RequestError

CARD_TYPES = ("visitor", "student", "staff")
STATUSES = ("requested", "approved", "issued", "returned")
ASCII_DIGITS = "0123456789"


def is_valid_id(value):
    """Check that an ID contains A followed by at least 3 ASCII digits."""
    if not isinstance(value, str) or len(value) < 4 or value[0] != "A":
        return False

    digits = value[1:]

    return (
        all(char in ASCII_DIGITS for char in digits)
        and any(char != "0" for char in digits)
    )


def make_id(number):
    """Generate an ID such as A001 or A1000."""
    return "A%03d" % number


def _clean_text(value, label):
    """Reject non-string or blank text."""
    if not isinstance(value, str) or not value.strip():
        raise RequestError("%s must not be blank." % label)

    return value.strip()


class RequestManager:
    def __init__(self):
        self._requests = {}
        self._next = 1

    def _get(self, request_id):
        if not is_valid_id(request_id):
            raise RequestError(
                "Malformed ID %r (expected e.g. A001)." % (request_id,)
            )

        if request_id not in self._requests:
            raise RequestError("Unknown ID %s." % request_id)

        return self._requests[request_id]

    def create(self, fellow_id, card_type):
        fellow_id = _clean_text(fellow_id, "Fellow ID")

        if not isinstance(card_type, str) or card_type not in CARD_TYPES:
            raise RequestError(
                "Invalid card type; allowed: %s." % ", ".join(CARD_TYPES)
            )

        record = {
            "id": make_id(self._next),
            "fellow_id": fellow_id,
            "card_type": card_type,
            "status": "requested",
            "approved_by": None,
        }

        self._requests[record["id"]] = record
        self._next += 1

        return dict(record)

    def view(self, request_id):
        return dict(self._get(request_id))

    def approve(self, request_id, approver):
        record = self._get(request_id)
        approver = _clean_text(approver, "Approver")

        self._require(record, "requested", "approve")

        record["status"] = "approved"
        record["approved_by"] = approver

        return dict(record)

    def issue(self, request_id):
        record = self._get(request_id)

        self._require(record, "approved", "issue")

        approver = record["approved_by"]

        if not isinstance(approver, str) or not approver.strip():
            raise RequestError(
                "%s has no approver; cannot issue." % request_id
            )

        record["status"] = "issued"

        return dict(record)

    def return_card(self, request_id):
        record = self._get(request_id)

        self._require(record, "issued", "return")
        record["status"] = "returned"

        return dict(record)

    @staticmethod
    def _require(record, needed, action):
        if record["status"] != needed:
            raise RequestError(
                "Cannot %s %s: status is '%s', must be '%s'."
                % (action, record["id"], record["status"], needed)
            )

    def list(self, status=None):
        if status is not None and (
            not isinstance(status, str) or status not in STATUSES
        ):
            raise RequestError("Unknown status %r." % status)

        return [
            dict(record)
            for record in self._requests.values()
            if status is None or record["status"] == status
        ]

    def to_dict(self):
        return {
            "requests": self.list(),
            "next_id": self._next,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise RequestError("Saved data must be a dictionary.")

        if set(data) != {"requests", "next_id"}:
            raise RequestError(
                "Saved data must contain requests and next_id only."
            )

        requests = data["requests"]
        next_id = data["next_id"]

        if not isinstance(requests, list):
            raise RequestError("Saved requests must be a list.")

        if type(next_id) is not int or next_id < 1:
            raise RequestError("Invalid next ID.")

        manager = cls()
        seen_ids = set()

        for record in requests:
            if not isinstance(record, dict):
                raise RequestError("Each request must be a dictionary.")

            required = {
                "id",
                "fellow_id",
                "card_type",
                "status",
                "approved_by",
            }

            if set(record) != required:
                raise RequestError(
                    "Request has missing or unexpected fields."
                )

            request_id = record["id"]

            if not is_valid_id(request_id):
                raise RequestError("Malformed request ID.")

            if request_id in seen_ids:
                raise RequestError("Duplicate request ID: %s" % request_id)

            fellow_id = record["fellow_id"]

            if (
                not isinstance(fellow_id, str)
                or not fellow_id.strip()
                or fellow_id != fellow_id.strip()
            ):
                raise RequestError("Invalid fellow ID.")

            card_type = record["card_type"]

            if not isinstance(card_type, str) or card_type not in CARD_TYPES:
                raise RequestError("Invalid card type.")

            status = record["status"]

            if not isinstance(status, str) or status not in STATUSES:
                raise RequestError("Invalid request status.")

            approver = record["approved_by"]

            if status == "requested":
                if approver is not None:
                    raise RequestError(
                        "Requested records must have no approver."
                    )
            elif (
                not isinstance(approver, str)
                or not approver.strip()
                or approver != approver.strip()
            ):
                raise RequestError(
                    "Approved, issued, and returned records "
                    "require a valid approver."
                )

            seen_ids.add(request_id)
            manager._requests[request_id] = dict(record)

        expected_next = (
            max(
                (int(request_id[1:]) for request_id in seen_ids),
                default=0,
            )
            + 1
        )

        if next_id < expected_next:
            raise RequestError(
                "Next ID would duplicate an existing request."
            )

        manager._next = next_id

        return manager