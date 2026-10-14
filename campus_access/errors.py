class RequestError(Exception):
    """Raised when an access-card request operation is invalid."""


class DataError(Exception):
    """Raised when saving or loading request data fails."""