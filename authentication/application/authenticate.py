from dependency_injector.wiring import (
    Provide, inject,
)

from authentication.application.exceptions.authentication import AuthenticationError
from authentication.domain.auth_provider import AuthProvider
from authentication.domain.exceptions.auth_provider import (
    InvalidTokenError,
    NotVerifiedEmailError,
)
from authentication.models import User
from authentication.dependency_injection.containers import Container
from authentication.dependency_injection.decorators import wire


class AuthenticationService:

    # TODO: Move dependency injection to infrastructure layer
    @wire
    @inject
    def __init__(self, auth_provider: AuthProvider = Provide[Container.auth_provider]):
        self._auth_provider = auth_provider

    def authenticate(self, auth_token):
        try:
            # TODO: Convert uid to provider_id in the model
            provider_user_id = self._auth_provider.get_user_id(auth_token)
            user = User.objects.get(uid=provider_user_id)
            user._id = str(user._id)
            return user
        except InvalidTokenError as e:
            raise AuthenticationError(str(e), 'INVALID_TOKEN')
        except NotVerifiedEmailError as e:
            raise AuthenticationError(str(e), 'EMAIL_NOT_VERIFIED')
        except User.DoesNotExist as e:
            raise AuthenticationError(str(e), 'UNREGISTERED_USER')
