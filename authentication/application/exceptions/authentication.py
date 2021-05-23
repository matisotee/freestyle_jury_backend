class AuthenticationError(Exception):

    def __init__(self, message, code):
        self.code = code
        self.message = message
        super().__init__(message)
