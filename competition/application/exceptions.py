class CompetitionApplicationError(Exception):

    def __init__(self, message: str, code: str):
        self.code = code
        self.message = message
        super().__init__(message)
