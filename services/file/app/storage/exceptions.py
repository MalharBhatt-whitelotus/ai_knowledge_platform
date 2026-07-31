class StorageError(Exception):
    """Base storage exception."""
    pass

class StorageFileNotFound(StorageError):
    """Raised when a file is not found."""
    pass