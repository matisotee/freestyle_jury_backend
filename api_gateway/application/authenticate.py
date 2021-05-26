from dependency_injector.wiring import (
    Provide, inject,
)

from shared.dependency_injection.container import Container

from api_gateway.application.exceptions.authentication import AuthenticationError
from api_gateway.domain.auth_provider import AuthProvider
from api_gateway.domain.exceptions.auth_provider import (
    InvalidTokenError,
    NotVerifiedEmailError,
)
from api_gateway.domain.models import User


class AuthenticationService:

    # TODO: Move dependency injection to infrastructure layer
    @inject
    def __init__(self, auth_provider: AuthProvider = Provide[Container.auth_provider]):
        self._auth_provider = auth_provider

    def authenticate(self, auth_token):
        try:
            provider_user_data = self._auth_provider.get_user_data(auth_token)
            user = User.objects.get(provider_id=provider_user_data.id)
            user.set_unusable_password()
            user._id = str(user._id)
            return user
        except InvalidTokenError as e:
            raise AuthenticationError(str(e), 'INVALID_TOKEN')
        except NotVerifiedEmailError as e:
            raise AuthenticationError(str(e), 'EMAIL_NOT_VERIFIED')
        except User.DoesNotExist as e:
            raise AuthenticationError(str(e), 'UNREGISTERED_USER')
