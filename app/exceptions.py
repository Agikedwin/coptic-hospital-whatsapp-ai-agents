class CRUDConflictError(Exception):
    """Raised when a database integrity rule rejects a mutation."""


class CRUDNotFoundError(Exception):
    """Raised when a requested database row does not exist."""
