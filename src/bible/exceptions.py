class InvalidArgumentsError(Exception):
    """Raised when arguments are not valid"""

    def __init__(self, message="Invalid arguments"):
        self.message = message
        super().__init__(message)
