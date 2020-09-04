from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class Authenticator:
    """
    The responsibility of this class is login and logout
    an user
    """

    @staticmethod
    def login(email, password):
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials', code='INVALID_CREDENTIALS')
        if not user.is_verified:
            raise AuthenticationFailed('Account is not verified', code='ACCOUNT_NOT_VERIFIED')

        logged_user = {
            'email': user.email,
            'name': user.name,
            'last_name': user.last_name,
            'aka': user.aka,
        }
        logged_user.update(user.get_tokens())

        return logged_user
