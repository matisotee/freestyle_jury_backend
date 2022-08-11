from firebase_admin import auth, credentials, initialize_app
from api_gateway.domain.auth_provider import AuthProvider, ProviderUserData
from api_gateway.domain.exceptions.auth_provider import InvalidTokenError, NotVerifiedEmailError
from shared.settings import settings


class FirebaseAuthProvider(AuthProvider):

    is_initialized = False

    def get_user_data(self, token: str) -> ProviderUserData:
        """
        Returns a firebase user id that matches the token
        """
        payload = self.get_user_info_by_firebase_token(token)

        firebase_user = auth.get_user(payload.get('uid'))

        if payload["firebase"]["sign_in_provider"] == "anonymous":
            raise InvalidTokenError('Firebase', 'Anonymous user')

        if settings.FIREBASE_AUTH['EMAIL_VERIFICATION'] and not firebase_user.email_verified:
            raise NotVerifiedEmailError('Firebase')

        user_data = ProviderUserData(
            id=firebase_user.uid,
            email=firebase_user.email if firebase_user.email is not None else '',
            phone_number=firebase_user.phone_number if firebase_user.phone_number is not None else ''
        )

        return user_data

    @classmethod
    def initialize_credentials(cls):
        cred = credentials.Certificate(settings.FIREBASE_AUTH['SERVICE_ACCOUNT_KEY_FILE'])
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
            raise InvalidTokenError('Firebase', 'Invalid format')
        except (
            auth.ExpiredIdTokenError,
            auth.InvalidIdTokenError,
            auth.RevokedIdTokenError,
        ):
            raise InvalidTokenError('Firebase')

        return payload
