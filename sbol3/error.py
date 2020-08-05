
class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class ValidationError(Error):

    def __init__(self, message: str):
        self.message = message
