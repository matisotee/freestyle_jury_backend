from unittest.mock import patch, MagicMock

import pytest
from rest_framework.exceptions import AuthenticationFailed

from firebase_admin import auth

import authentication
from authentication.firebase_connector import FirebaseConnector


@patch(
    'authentication.firebase_connector.auth.verify_id_token',
    return_value={'test_user_info': '1234'}
)
def test_get_user_info_by_firebase_token_success(mock_firebase):
    FirebaseConnector.is_initialized = True

    result = FirebaseConnector.get_user_info_by_firebase_token('test_token')

    assert mock_firebase.called
    assert result == {'test_user_info': '1234'}


@patch(
    'authentication.firebase_connector.auth.verify_id_token',
    side_effect=ValueError()
)
def test_get_user_info_by_firebase_with_invalid_token(mock_firebase):
    FirebaseConnector.is_initialized = True
    with pytest.raises(AuthenticationFailed):
        FirebaseConnector.get_user_info_by_firebase_token('test_token')


@patch(
    'authentication.firebase_connector.auth.verify_id_token',
    side_effect=auth.ExpiredIdTokenError('test_message', 'TEST_CODE')
)
def test_get_user_info_by_firebase_with_expired_token(mock_firebase):
    FirebaseConnector.is_initialized = True
    with pytest.raises(AuthenticationFailed):
        FirebaseConnector.get_user_info_by_firebase_token('test_token')


@patch(
    'authentication.firebase_connector.auth.get_user',
)
def test_authenticate_in_firebase_success(mock_get_user):
    user_info = {
        'uid': 'test_uid',
        'firebase': {
            'sign_in_provider': 'mail'
        }
    }
    mock_firebase_user = MagicMock()
    mock_firebase_user.email_verified = True
    mock_get_user.return_value = mock_firebase_user
    authentication.firebase_connector.firebase_auth_settings.EMAIL_VERIFICATION = True

    with patch.object(
        FirebaseConnector,
        'get_user_info_by_firebase_token',
        return_value=user_info
    ):
        result = FirebaseConnector.authenticate_in_firebase('test_token')

    assert result == user_info
    assert mock_get_user.called


@patch(
    'authentication.firebase_connector.auth.get_user',
)
def test_authenticate_in_firebase_with_anonymous_user_fails(mock_get_user):
    user_info = {
        'uid': 'test_uid',
        'firebase': {
            'sign_in_provider': 'anonymous'
        }
    }

    with patch.object(
            FirebaseConnector,
            'get_user_info_by_firebase_token',
            return_value=user_info
    ):
        with pytest.raises(AuthenticationFailed):
            FirebaseConnector.authenticate_in_firebase('test_token')


@patch(
    'authentication.firebase_connector.auth.get_user',
)
def test_authenticate_in_firebase_with_email_not_verified_fails(mock_get_user):
    user_info = {
        'uid': 'test_uid',
        'firebase': {
            'sign_in_provider': 'mail'
        }
    }
    mock_firebase_user = MagicMock()
    mock_firebase_user.email_verified = False
    mock_get_user.return_value = mock_firebase_user
    authentication.firebase_connector.firebase_auth_settings.EMAIL_VERIFICATION = True

    with patch.object(
            FirebaseConnector,
            'get_user_info_by_firebase_token',
            return_value=user_info
    ):
        with pytest.raises(AuthenticationFailed):
            FirebaseConnector.authenticate_in_firebase('test_token')


@patch('authentication.firebase_connector.credentials')
@patch('authentication.firebase_connector.initialize_app')
def test_initialize_credentials(mock_init, mock_cred):

    FirebaseConnector.initialize_credentials()

    assert mock_cred.Certificate.called
    assert mock_init.called
    assert FirebaseConnector.is_initialized
