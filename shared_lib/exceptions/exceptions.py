class AppException(Exception):
    """
    Base exception for all application errors.
    """
    def __init__(self, code, message, status_code):
        self.code = code
        self.message = message
        self.status_code = status_code