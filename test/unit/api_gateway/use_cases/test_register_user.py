from unittest.mock import MagicMock

import pytest
from test.utils import generate_object_id

from api_gateway.domain.exceptions.user import ExistingUserError

from api_gateway.application.exceptions.registration import RegistrationError
from api_gateway.application.register_user import UserRegistrar
from api_gateway.domain.auth_provider import ProviderUserData
from api_gateway.domain.exceptions.auth_provider import InvalidTokenError, NotVerifiedEmailError
from api_gateway.domain.user import User


def test_register_user():
    expected_user = User(
        id=str(generate_object_id()),
        name='test_name',
        last_name='test_last_name',
        aka='test_aka',
        email='test@test.com',
        provider_id='1234',
        phone_number='',
    )
    mock_provider = MagicMock()
    mock_provider.get_user_data.return_value = ProviderUserData(
        id=expected_user.provider_id, email=expected_user.email, phone_number=''
    )
    mock_user_repository = MagicMock()
    mock_user_repository.create.return_value = expected_user
    registrar = UserRegistrar(auth_provider=mock_provider, user_repository=mock_user_repository)

    result = registrar.register_user(
        expected_user.name, expected_user.last_name, 'test_token', expected_user.aka
    )

    assert result.name == expected_user.name
    assert result.last_name == expected_user.last_name
    assert result.aka == expected_user.aka
    assert result.email == expected_user.email
    assert result.phone_number == ''
    mock_provider.get_user_data.assert_called_once_with('test_token')
    assert mock_user_repository.create.call_args[0][0].email == expected_user.email


def test_register_user_with_invalid_token():
    mock_provider = MagicMock()
    mock_provider.get_user_data.side_effect = InvalidTokenError('test_provider')
    registrar = UserRegistrar(auth_provider=mock_provider)

    with pytest.raises(RegistrationError) as ex_info:
        registrar.register_user(
            'test_name', 'test_last_name', 'test_token', 'test_aka'
        )

    exception = ex_info.value
    assert exception.code == 'INVALID_TOKEN'


def test_register_user_with_not_verified_user():
    mock_provider = MagicMock()
    mock_provider.get_user_data.side_effect = NotVerifiedEmailError('test_provider')
    registrar = UserRegistrar(auth_provider=mock_provider)

    with pytest.raises(RegistrationError) as ex_info:
        registrar.register_user(
            'test_name', 'test_last_name', 'test_token', 'test_aka'
        )

    exception = ex_info.value
    assert exception.code == 'EMAIL_NOT_VERIFIED'


def test_register_user_with_existent_user():
    mock_provider = MagicMock()
    mock_provider.get_user_data.return_value = ProviderUserData(
        id='1234', email='test@test.com', phone_number=''
    )
    mock_user_repository = MagicMock()
    mock_user_repository.create.side_effect = ExistingUserError()
    registrar = UserRegistrar(auth_provider=mock_provider, user_repository=mock_user_repository)

    with pytest.raises(RegistrationError) as ex_info:
        registrar.register_user(
            'test_name', 'test_last_name', 'test_token', 'test_aka'
        )

    exception = ex_info.value
    assert exception.code == 'USER_ALREADY_EXISTS'
