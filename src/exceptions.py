class InvalidArgumentsError(Exception):
    """Raised when arguments are not valid"""

    message: str

    def __init__(self, message: str="Invalid arguments"):
        self.message = message
        super().__init__(message)
