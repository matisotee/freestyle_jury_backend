from django.utils.translation import gettext as _
from rest_framework import exceptions

from firebase_admin import auth
from firebase_admin import credentials, initialize_app
from firebase_auth.settings import firebase_auth_settings

is_initialized = False


def initialize_credentials():
    cred = credentials.Certificate(firebase_auth_settings.SERVICE_ACCOUNT_KEY_FILE)
    try:
        initialize_app(cred)
    except:
        pass

    is_initialized = True


def get_user_info_by_firebase_token(firebase_token):

    if not is_initialized:
        initialize_credentials()

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


def authenticate_in_firebase(firebase_token):
    """
    Returns an user that matches the payload's user uid and email.
    """
    payload = get_user_info_by_firebase_token(firebase_token)

    firebase_user = auth.get_user(payload.get('uid'))

    if payload["firebase"]["sign_in_provider"] == "anonymous":
        msg = _("Firebase anonymous sign-in is not supported.")
        raise exceptions.AuthenticationFailed(msg)

    if firebase_auth_settings.EMAIL_VERIFICATION and not firebase_user.email_verified:
        msg = _("User email not yet confirmed.")
        raise exceptions.AuthenticationFailed(msg)

    return payload
