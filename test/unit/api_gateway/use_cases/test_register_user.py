from unittest.mock import MagicMock, patch

import pytest

from api_gateway.application.exceptions.registration import RegistrationError
from api_gateway.application.register_user import UserRegistrar
from api_gateway.domain.auth_provider import ProviderUserData
from api_gateway.domain.exceptions.auth_provider import InvalidTokenError, NotVerifiedEmailError
from api_gateway.models import UserManager, User


@patch.object(User, 'clean_fields')
@patch.object(User, 'save')
@patch.object(UserManager, 'filter')
def test_register_user(mock_filter, mock_save, mock_clean):
    mock_filter.return_value.exists.return_value = False
    registrar = UserRegistrar()
    mock_provider = MagicMock()
    mock_provider.get_user_data.return_value = ProviderUserData(
        id='1234', email='test@test.com', phone_number=''
    )
    registrar._auth_provider = mock_provider

    result = registrar.register_user(
        'test_name', 'test_last_name', 'test_token', 'test_aka'
    )

    assert result['name'] == 'test_name'
    assert result['last_name'] == 'test_last_name'
    assert result['aka'] == 'test_aka'
    assert result['email'] == 'test@test.com'
    assert result['phone_number'] == ''


def test_register_user_with_invalid_token():
    registrar = UserRegistrar()
    mock_provider = MagicMock()
    mock_provider.get_user_data.side_effect = InvalidTokenError('test_provider')
    registrar._auth_provider = mock_provider

    with pytest.raises(RegistrationError) as ex_info:
        registrar.register_user(
            'test_name', 'test_last_name', 'test_token', 'test_aka'
        )

    exception = ex_info.value
    assert exception.code == 'INVALID_TOKEN'


def test_register_user_with_not_verified_user():
    registrar = UserRegistrar()
    mock_provider = MagicMock()
    mock_provider.get_user_data.side_effect = NotVerifiedEmailError('test_provider')
    registrar._auth_provider = mock_provider

    with pytest.raises(RegistrationError) as ex_info:
        registrar.register_user(
            'test_name', 'test_last_name', 'test_token', 'test_aka'
        )

    exception = ex_info.value
    assert exception.code == 'EMAIL_NOT_VERIFIED'


@patch.object(User, 'clean_fields')
@patch.object(User, 'save')
@patch.object(UserManager, 'filter')
def test_register_user_with_existent_user(mock_filter, mock_save, mock_clean):
    mock_filter.return_value.exists.return_value = True
    registrar = UserRegistrar()
    mock_provider = MagicMock()
    mock_provider.get_user_data.return_value = ProviderUserData(
        id='1234', email='test@test.com', phone_number=''
    )
    registrar._auth_provider = mock_provider

    with pytest.raises(RegistrationError) as ex_info:
        registrar.register_user(
            'test_name', 'test_last_name', 'test_token', 'test_aka'
        )

    exception = ex_info.value
    assert exception.code == 'USER_ALREADY_EXISTS'