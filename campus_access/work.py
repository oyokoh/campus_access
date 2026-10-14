from campus_access.errors import RequestError


CARD_TYPES = ("visitor", "student", "staff")

STATUSES = ("requested", "approved", "issued", "returned")

ASCII_DIGITS = "0123456789"


def is_valid_id(value):
    """Check that an ID contains A followed by at least 3 ASCII digits."""
    if not isinstance(value, str) or len(value) < 4 or value[0] != "A":
        return False

    digits = value[1:]

    return all(char in ASCII_DIGITS for char in digits) and int(digits) >= 1


def make_id(number):
    """Generate a request ID such as A001 or A1000."""
    return "A%03d" % number


def _clean_text(value, label):
    """Reject values that are not strings or contain only whitespace."""
    if not isinstance(value, str) or not value.strip():
        raise RequestError("%s must not be blank." % label)

    return value.strip()


class RequestManager:
    """Manage access-card requests and their workflow."""

    def __init__(self):
        self._requests = {}
        self._next = 1

    def _get(self, request_id):
        """Find a request or reject an invalid or unknown ID."""
        if not is_valid_id(request_id):
            raise RequestError(
                "Malformed ID %r (expected e.g. A001)." % (request_id,)
            )

        if request_id not in self._requests:
            raise RequestError("Unknown ID %s." % request_id)

        return self._requests[request_id]

    def create(self, fellow_id, card_type):
        """Create a new access-card request."""
        fellow_id = _clean_text(fellow_id, "Fellow ID")

        if card_type not in CARD_TYPES:
            raise RequestError(
                "Invalid card type %r; allowed: %s."
                % (card_type, ", ".join(CARD_TYPES))
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
        """Return a copy of a request."""
        return dict(self._get(request_id))

    def approve(self, request_id, approver):
        """Approve a request that is currently requested."""
        record = self._get(request_id)
        approver = _clean_text(approver, "Approver")

        self._require(record, "requested", "approve")

        record["status"] = "approved"
        record["approved_by"] = approver

        return dict(record)

    def issue(self, request_id):
        """Issue a card only after approval."""
        record = self._get(request_id)

        self._require(record, "approved", "issue")

        if not isinstance(record["approved_by"], str) or not record["approved_by"].strip():
            raise RequestError(
                "%s has no approver; cannot issue." % request_id
            )

        record["status"] = "issued"

        return dict(record)

    def return_card(self, request_id):
        """Return a card that has already been issued."""
        record = self._get(request_id)

        self._require(record, "issued", "return")

        record["status"] = "returned"

        return dict(record)

    @staticmethod
    def _require(record, needed, action):
        """Reject an operation if the request is in the wrong state."""
        if record["status"] != needed:
            raise RequestError(
                "Cannot %s %s: status is '%s', must be '%s'."
                % (
                    action,
                    record["id"],
                    record["status"],
                    needed,
                )
            )

    def list(self, status=None):
        """Return all requests, optionally filtered by status."""
        if status is not None and status not in STATUSES:
            raise RequestError("Unknown status %r." % status)

        return [
            dict(record)
            for record in self._requests.values()
            if status is None or record["status"] == status
        ]

    def to_dict(self):
        """Return a copy of the manager's data for storage."""
        return {
            "requests": self.list(),
            "next_id": self._next,
        }    
        