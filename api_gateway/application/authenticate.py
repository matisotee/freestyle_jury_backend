from dependency_injector.wiring import (
    Provide, inject,
)

from api_gateway.application.exceptions.authentication import AuthenticationError
from api_gateway.domain.auth_provider import AuthProvider
from api_gateway.domain.exceptions.auth_provider import (
    InvalidTokenError,
    NotVerifiedEmailError,
)
from api_gateway.domain.exceptions.user import NotExistentUserError
from api_gateway.domain.repositories import UserRepository
from api_gateway.infrastructure.django.dependency_injection import Container


class AuthenticationService:

    # TODO: Move dependency injection to infrastructure layer
    @inject
    def __init__(
            self,
            auth_provider: AuthProvider = Provide[Container.auth_provider],
            user_repository: UserRepository = Provide[Container.user_repository],
    ):
        self._auth_provider = auth_provider
        self._user_repository = user_repository

    def authenticate(self, auth_token):
        try:
            provider_user_data = self._auth_provider.get_user_data(auth_token)
            user = self._user_repository.get_by_provider_id(provider_user_data.id)
            return user
        except InvalidTokenError as e:
            raise AuthenticationError(str(e), 'INVALID_TOKEN')
        except NotVerifiedEmailError as e:
            raise AuthenticationError(str(e), 'EMAIL_NOT_VERIFIED')
        except NotExistentUserError as e:
            raise AuthenticationError(str(e), 'UNREGISTERED_USER')
