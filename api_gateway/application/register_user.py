from api_gateway.application.exceptions.registration import RegistrationError
from api_gateway.dependency_injection import Container
from api_gateway.domain.auth_provider import AuthProvider
from dependency_injector.wiring import inject, Provide

from api_gateway.dependency_injection.decorators import wire
from api_gateway.domain.exceptions.auth_provider import InvalidTokenError, NotVerifiedEmailError
from api_gateway.domain.exceptions.user import ExistingUserError
from api_gateway.models import User


class UserRegistrar:

    @wire
    @inject
    def __init__(self, auth_provider: AuthProvider = Provide[Container.auth_provider]):
        self._auth_provider = auth_provider

    def register_user(self, name: str, last_name: str, token: str, aka: str = '') -> dict:
        try:
            provider_user_data = self._auth_provider.get_user_data(token)
            user = User.objects.create_user(
                provider_user_data.id,
                name,
                last_name,
                provider_user_data.email,
                provider_user_data.phone_number,
                aka
            )
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
