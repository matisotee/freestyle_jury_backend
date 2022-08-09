from dependency_injector.wiring import inject, Provide

from api_gateway.application.exceptions.registration import RegistrationError
from api_gateway.domain.auth_provider import AuthProvider
from api_gateway.domain.exceptions.auth_provider import (
    InvalidTokenError, NotVerifiedEmailError,
)
from api_gateway.domain.exceptions.user import ExistingUserError
from api_gateway.domain.models import User
from api_gateway.domain.repositories import UserRepository
from api_gateway.infrastructure.django.dependency_injection import Container


class UserRegistrar:

    @inject
    def __init__(
            self,
            auth_provider: AuthProvider = Provide[Container.auth_provider],
            user_repository: UserRepository = Provide[Container.user_repository],
    ):
        self._auth_provider = auth_provider
        self._repository = user_repository

    def register_user(self, name: str, last_name: str, token: str, aka: str = '') -> dict:
        try:
            provider_user_data = self._auth_provider.get_user_data(token)
            user = User(
                provider_id=provider_user_data.id,
                name=name,
                last_name=last_name,
                email=provider_user_data.email,
                phone_number=provider_user_data.phone_number,
                aka=aka
            )
            user = self._repository.create(user)
        except InvalidTokenError as e:
            raise RegistrationError(str(e), 'INVALID_TOKEN')
        except NotVerifiedEmailError as e:
            raise RegistrationError(str(e), 'EMAIL_NOT_VERIFIED')
        except ExistingUserError as e:
            raise RegistrationError(str(e), 'USER_ALREADY_EXISTS')

        return self._map_user_to_dict(user)

    @staticmethod
    def _map_user_to_dict(user):
        return {
            'id': str(user._id),
            'name': user.name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user.phone_number,
            'aka': user.aka
        }
