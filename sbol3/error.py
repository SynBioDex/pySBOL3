
class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class SBOLError(Error):

    def __init__(self, message: str):
        self.message = message


class NamespaceError(Error):
    """Exception raised for namespace errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str):
        self.message = message
