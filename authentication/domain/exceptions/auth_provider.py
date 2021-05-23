class InvalidTokenError(Exception):

    def __init__(self, provider_name: str, reason: str = ''):
        super().__init__(f'The token provided to {provider_name} is invalid. {reason}')


class NotVerifiedEmailError(Exception):

    def __init__(self, provider_name: str):
        super().__init__(f"The user's email was not verified in {provider_name}")
