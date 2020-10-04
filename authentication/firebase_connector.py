from django.utils.translation import gettext as _
from rest_framework import exceptions

from firebase_admin import auth, credentials, initialize_app
from firebase_auth.settings import firebase_auth_settings


class FirebaseConnector:

    is_initialized = False

    @classmethod
    def initialize_credentials(cls):
        cred = credentials.Certificate(firebase_auth_settings.SERVICE_ACCOUNT_KEY_FILE)
        try:
            initialize_app(cred)
        finally:
            pass

        cls.is_initialized = True

    @classmethod
    def get_user_info_by_firebase_token(cls, firebase_token):

        if not cls.is_initialized:
            cls.initialize_credentials()

        try:
            payload = auth.verify_id_token(firebase_token)
        except ValueError:
            msg = _("Invalid firebase ID token.")
            raise exceptions.AuthenticationFailed(msg)
        except (
            auth.ExpiredIdTokenError,
            auth.InvalidIdTokenError,
            auth.RevokedIdTokenError,
        ):
            msg = _("Could not log in.")
            raise exceptions.AuthenticationFailed(msg, 'INVALID_TOKEN')

        return payload

    @classmethod
    def authenticate_in_firebase(cls, firebase_token):
        """
        Returns an user that matches the payload's user uid and email.
        """
        payload = cls.get_user_info_by_firebase_token(firebase_token)

        firebase_user = auth.get_user(payload.get('uid'))

        if payload["firebase"]["sign_in_provider"] == "anonymous":
            msg = _("Firebase anonymous sign-in is not supported.")
            raise exceptions.AuthenticationFailed(msg)

        if firebase_auth_settings.EMAIL_VERIFICATION and not firebase_user.email_verified:
            msg = _("User email not yet confirmed.")
            raise exceptions.AuthenticationFailed(msg)

        return payload
