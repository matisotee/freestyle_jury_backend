from unittest.mock import MagicMock

import pytest

from api_gateway.application.authenticate import AuthenticationService
from api_gateway.application.exceptions.authentication import AuthenticationError
from api_gateway.domain.auth_provider import ProviderUserData
from api_gateway.domain.exceptions.auth_provider import InvalidTokenError, NotVerifiedEmailError
from api_gateway.domain.exceptions.user import NotExistentUserError
from api_gateway.domain.user import User
from test.utils import generate_object_id


def test_authenticate():
    expected_user = User(
        _id=generate_object_id(), provider_id='1234', name='test',
        last_name='test', email='test@test.com', aka='tes'
    )
    mock_user_repository = MagicMock()
    mock_user_repository.get_by_provider_id.return_value = expected_user
    mock_auth_provider = MagicMock()
    mock_auth_provider.get_user_data.return_value = ProviderUserData(
        id='1234', email='test@test.com', phone_number=''
    )
    auth_service = AuthenticationService(auth_provider=mock_auth_provider, user_repository=mock_user_repository)

    result = auth_service.authenticate('test_token')

    assert result == expected_user
    mock_auth_provider.get_user_data.assert_called_once_with('test_token')
    mock_user_repository.get_by_provider_id.assert_called_once_with(expected_user.provider_id)


def test_authenticate_with_invalid_token():
    mock_auth_provider = MagicMock()
    mock_auth_provider.get_user_data.side_effect = InvalidTokenError('Test')
    auth_service = AuthenticationService(auth_provider=mock_auth_provider)

    with pytest.raises(AuthenticationError):
        auth_service.authenticate('test_token')


def test_authenticate_with_unverified_email():
    mock_auth_provider = MagicMock()
    mock_auth_provider.get_user_data.side_effect = NotVerifiedEmailError('Test')
    auth_service = AuthenticationService(auth_provider=mock_auth_provider)

    with pytest.raises(AuthenticationError):
        auth_service.authenticate('test_token')


def test_authenticate_with_unregistered_user():
    expected_user = User(
        _id=generate_object_id(), provider_id='1234', name='test',
        last_name='test', email='test@test.com', aka='tes'
    )
    mock_auth_provider = MagicMock()
    mock_auth_provider.get_by_provider_id.return_value = expected_user
    mock_user_repository = MagicMock()
    mock_user_repository.get_by_provider_id.side_effect = NotExistentUserError()
    auth_service = AuthenticationService(auth_provider=mock_auth_provider, user_repository=mock_user_repository)

    with pytest.raises(AuthenticationError):
        auth_service.authenticate('test_token')
