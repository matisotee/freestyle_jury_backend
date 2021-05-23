from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header, BaseAuthentication

from authentication.application.authenticate import AuthenticationService
from authentication.application.exceptions.authentication import AuthenticationError


class DjangoAuthentication(BaseAuthentication):
    www_authenticate_realm = "api"
    auth_header_prefix = "Bearer"

    def authenticate(self, request):
        auth_token = self._get_token_from_header(request)

        try:
            authentication_service = AuthenticationService()
            user = authentication_service.authenticate(auth_token)
        except AuthenticationError as e:
            raise exceptions.AuthenticationFailed(e.message, code=e.code)
        return user, None

    def _get_token_from_header(self, request):
        """
        Returns the auth token from request.
        """
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.auth_header_prefix.lower().encode():
            raise exceptions.AuthenticationFailed(
                'Invalid Authorization header: No credentials provided.',
                code='NO_TOKEN_PROVIDED'
            )

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed(
                'Invalid Authorization header: No credentials provided.',
                code='NO_TOKEN_PROVIDED'
            )
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed(
                'Invalid Authorization header: Token string should not contain spaces.',
                code='INVALID_TOKEN'
            )

        return auth[1]

    def authenticate_header(self, request):
        return '{} realm="{}"'.format(
            self.auth_header_prefix, self.www_authenticate_realm
        )
