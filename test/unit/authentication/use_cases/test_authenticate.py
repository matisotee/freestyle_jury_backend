from unittest.mock import patch, MagicMock

import pytest

from authentication.application.authenticate import AuthenticationService
from authentication.application.exceptions.authentication import AuthenticationError
from authentication.domain.exceptions.auth_provider import InvalidTokenError, NotVerifiedEmailError
from authentication.models import UserManager, User


@patch.object(UserManager, 'get')
def test_authenticate(mock_get_user):
    expected_user = User(
        _id='5678', uid='1234', name='test', last_name='test', aka='tes'
    )
    mock_get_user.return_value = expected_user
    mock_auth_provider = MagicMock()
    mock_auth_provider.get_user_id.return_value = '1234'
    auth_service = AuthenticationService()
    auth_service._auth_provider = mock_auth_provider

    result = auth_service.authenticate('test_token')

    assert result == expected_user
    mock_auth_provider.get_user_id.assert_called()
    mock_get_user.assert_called()


def test_authenticate_with_invalid_token():
    mock_auth_provider = MagicMock()
    mock_auth_provider.get_user_id.side_effect = InvalidTokenError('Test')
    auth_service = AuthenticationService()
    auth_service._auth_provider = mock_auth_provider

    with pytest.raises(AuthenticationError):
        auth_service.authenticate('test_token')


def test_authenticate_with_unverified_email():
    mock_auth_provider = MagicMock()
    mock_auth_provider.get_user_id.side_effect = NotVerifiedEmailError('Test')
    auth_service = AuthenticationService()
    auth_service._auth_provider = mock_auth_provider

    with pytest.raises(AuthenticationError):
        auth_service.authenticate('test_token')


@patch.object(UserManager, 'get')
def test_authenticate_with_unregistered_user(mock_get_user):
    mock_get_user.side_effect = User.DoesNotExist
    mock_auth_provider = MagicMock()
    mock_auth_provider.get_user_id.side_effect = NotVerifiedEmailError('Test')
    auth_service = AuthenticationService()
    auth_service._auth_provider = mock_auth_provider

    with pytest.raises(AuthenticationError):
        auth_service.authenticate('test_token')
