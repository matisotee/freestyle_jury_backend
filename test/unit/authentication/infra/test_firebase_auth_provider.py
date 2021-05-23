from unittest.mock import patch, MagicMock

import pytest

from firebase_admin import auth

import authentication
from authentication.domain.exceptions.auth_provider import (
    InvalidTokenError,
    NotVerifiedEmailError,
)
from authentication.infrastructure.authentication.firebase_auth_provider import FirebaseAuthProvider


@patch(
    'authentication.infrastructure.authentication.firebase_auth_provider.auth.get_user',
)
@patch(
    'authentication.infrastructure.authentication.firebase_auth_provider.auth.verify_id_token',
    return_value={
        'firebase': {'sign_in_provider': 'password'},
        'uid': '1234'
    }
)
def test_get_user_id_success(mock_user_data, mock_get_user):
    FirebaseAuthProvider.is_initialized = True
    mock_get_user.return_value.email_verified = True
    auth_provider = FirebaseAuthProvider()

    result = auth_provider.get_user_id('test_token')

    assert mock_user_data.called
    assert result == '1234'


@patch(
    'authentication.infrastructure.authentication.firebase_auth_provider.auth.verify_id_token',
    side_effect=ValueError()
)
def test_get_user_id_with_invalid_token(mock_firebase):
    FirebaseAuthProvider.is_initialized = True
    auth_provider = FirebaseAuthProvider()

    with pytest.raises(InvalidTokenError):
        auth_provider.get_user_id('test_token')


@patch(
    'authentication.infrastructure.authentication.firebase_auth_provider.auth.verify_id_token',
    side_effect=auth.ExpiredIdTokenError('test_message', 'TEST_CODE')
)
def test_get_user_id_with_expired_token(mock_firebase):
    FirebaseAuthProvider.is_initialized = True
    auth_provider = FirebaseAuthProvider()

    with pytest.raises(InvalidTokenError):
        auth_provider.get_user_id('test_token')


@patch(
    'authentication.infrastructure.authentication.firebase_auth_provider.auth.get_user',
)
@patch(
    'authentication.infrastructure.authentication.firebase_auth_provider.auth.verify_id_token',
    return_value={
        'firebase': {'sign_in_provider': 'anonymous'},
        'uid': '1234'
    }
)
def test_get_user_id_with_anonymous_user(mock_user_data, mock_get_user):
    FirebaseAuthProvider.is_initialized = True
    auth_provider = FirebaseAuthProvider()

    with pytest.raises(InvalidTokenError):
        auth_provider.get_user_id('test_token')


@patch(
    'authentication.infrastructure.authentication.firebase_auth_provider.auth.get_user',
)
@patch(
    'authentication.infrastructure.authentication.firebase_auth_provider.auth.verify_id_token',
    return_value={
        'firebase': {'sign_in_provider': 'password'},
        'uid': '1234'
    }
)
def test_get_user_id_with_email_not_verified(mock_user_data, mock_get_user):
    FirebaseAuthProvider.is_initialized = True
    mock_get_user.return_value.email_verified = False
    auth_provider = FirebaseAuthProvider()

    with pytest.raises(NotVerifiedEmailError):
        auth_provider.get_user_id('test_token')
