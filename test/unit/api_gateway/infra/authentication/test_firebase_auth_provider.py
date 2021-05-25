from unittest.mock import patch

import pytest

from firebase_admin import auth

from api_gateway.domain.exceptions.auth_provider import (
    InvalidTokenError,
    NotVerifiedEmailError,
)
from api_gateway.infrastructure.authentication.firebase_auth_provider import FirebaseAuthProvider


@patch(
    'api_gateway.infrastructure.authentication.firebase_auth_provider.auth.get_user',
)
@patch(
    'api_gateway.infrastructure.authentication.firebase_auth_provider.auth.verify_id_token',
    return_value={
        'firebase': {'sign_in_provider': 'password'},
        'uid': '1234'
    }
)
def test_get_user_data_success(mock_user_data, mock_get_user):
    FirebaseAuthProvider.is_initialized = True
    mock_get_user.return_value.email_verified = True
    mock_get_user.return_value.email = 'test@test.com'
    mock_get_user.return_value.phone_number = '123456'
    mock_get_user.return_value.uid = '1234'
    auth_provider = FirebaseAuthProvider()

    result = auth_provider.get_user_data('test_token')

    assert mock_user_data.called
    assert result.id == '1234'
    assert result.email == 'test@test.com'
    assert result.phone_number == '123456'


@patch(
    'api_gateway.infrastructure.authentication.firebase_auth_provider.auth.verify_id_token',
    side_effect=ValueError()
)
def test_get_user_data_with_invalid_token(mock_firebase):
    FirebaseAuthProvider.is_initialized = True
    auth_provider = FirebaseAuthProvider()

    with pytest.raises(InvalidTokenError):
        auth_provider.get_user_data('test_token')


@patch(
    'api_gateway.infrastructure.authentication.firebase_auth_provider.auth.verify_id_token',
    side_effect=auth.ExpiredIdTokenError('test_message', 'TEST_CODE')
)
def test_get_user_data_with_expired_token(mock_firebase):
    FirebaseAuthProvider.is_initialized = True
    auth_provider = FirebaseAuthProvider()

    with pytest.raises(InvalidTokenError):
        auth_provider.get_user_data('test_token')


@patch(
    'api_gateway.infrastructure.authentication.firebase_auth_provider.auth.get_user',
)
@patch(
    'api_gateway.infrastructure.authentication.firebase_auth_provider.auth.verify_id_token',
    return_value={
        'firebase': {'sign_in_provider': 'anonymous'},
        'uid': '1234'
    }
)
def test_get_user_data_with_anonymous_user(mock_user_data, mock_get_user):
    FirebaseAuthProvider.is_initialized = True
    auth_provider = FirebaseAuthProvider()

    with pytest.raises(InvalidTokenError):
        auth_provider.get_user_data('test_token')


@patch(
    'api_gateway.infrastructure.authentication.firebase_auth_provider.auth.get_user',
)
@patch(
    'api_gateway.infrastructure.authentication.firebase_auth_provider.auth.verify_id_token',
    return_value={
        'firebase': {'sign_in_provider': 'password'},
        'uid': '1234'
    }
)
def test_get_user_data_with_email_not_verified(mock_user_data, mock_get_user):
    FirebaseAuthProvider.is_initialized = True
    mock_get_user.return_value.email_verified = False
    auth_provider = FirebaseAuthProvider()

    with pytest.raises(NotVerifiedEmailError):
        auth_provider.get_user_data('test_token')
