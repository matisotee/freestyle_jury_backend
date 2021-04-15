class CallServiceError(Exception):

    def __init__(self, message, code):
        self.code = code
        super().__init__(message)
