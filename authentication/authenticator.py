from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header, BaseAuthentication

from authentication.firebase_connector import FirebaseConnector
from authentication.models import User


class FirebaseAuthentication(BaseAuthentication):
    """
    Implementation of token based authentication using firebase.
    """
    www_authenticate_realm = "api"
    auth_header_prefix = "Bearer"
    uid_field = User.USERNAME_FIELD

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and decoded firebase payload if a valid signature
        has been supplied. Otherwise returns `None`.
        """
        firebase_token = self.get_token(request)

        if not firebase_token:
            return None

        payload = FirebaseConnector.authenticate_in_firebase(firebase_token)
        user = self.get_user_by_uid(payload['uid'])

        return (user, payload)

    def get_token(self, request):
        """
        Returns the firebase ID token from request.
        """
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.auth_header_prefix.lower().encode():
            return None

        if len(auth) == 1:
            msg = _("Invalid Authorization header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _(
                "Invalid Authorization header. Token string should not contain spaces."
            )
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def get_user_by_uid(self, uid):

        try:
            user = User.objects.get(**{self.uid_field: uid})
        except User.DoesNotExist:
            msg = _("User not registered")
            raise exceptions.AuthenticationFailed(msg)

        return user

    def authenticate_header(self, request):
        return '{} realm="{}"'.format(
            self.auth_header_prefix, self.www_authenticate_realm
        )
