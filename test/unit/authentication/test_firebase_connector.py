from unittest.mock import patch, MagicMock

from django.test import TestCase
from rest_framework.exceptions import AuthenticationFailed

from firebase_admin import auth

from authentication.firebase_connector import get_user_info_by_firebase_token, authenticate_in_firebase


class FirebaseConnectorTest(TestCase):

    @patch('authentication.firebase_connector.is_initialized')
    @patch(
        'authentication.firebase_connector.auth.verify_id_token',
        return_value={'test_user_info': '1234'}
    )
    def test_get_user_info_by_firebase_token_success(self, mock_firebase, mock_is_initialized):
        mock_is_initialized = True

        result = get_user_info_by_firebase_token('test_token')

        self.assertTrue(mock_firebase.called)
        self.assertEqual(result, {'test_user_info': '1234'})

    @patch('authentication.firebase_connector.is_initialized')
    @patch(
        'authentication.firebase_connector.auth.verify_id_token',
        side_effect=ValueError()
    )
    def test_get_user_info_by_firebase_with_invalid_token(self, mock_firebase, mock_is_initialized):
        mock_is_initialized = True
        with self.assertRaises(AuthenticationFailed):
            get_user_info_by_firebase_token('test_token')

    @patch('authentication.firebase_connector.is_initialized')
    @patch(
        'authentication.firebase_connector.auth.verify_id_token',
        side_effect=auth.ExpiredIdTokenError('test_message', 'TEST_CODE')
    )
    def test_get_user_info_by_firebase_with_expired_token(self, mock_firebase, mock_is_initialized):
        mock_is_initialized = True
        with self.assertRaises(AuthenticationFailed):
            get_user_info_by_firebase_token('test_token')

    @patch(
        'authentication.firebase_connector.auth.get_user',
    )
    @patch(
        'authentication.firebase_connector.firebase_auth_settings.EMAIL_VERIFICATION',
    )
    def test_authenticate_in_firebase_success(
        self,
        mock_email_verification,
        mock_get_user,
    ):
        user_info = {
            'uid': 'test_uid',
            'firebase': {
                'sign_in_provider': 'mail'
            }
        }
        mock_firebase_user = MagicMock()
        mock_firebase_user.email_verified = True
        mock_get_user.return_value = mock_firebase_user
        mock_email_verification = True

        with patch(
            'authentication.firebase_connector.get_user_info_by_firebase_token',
            return_value=user_info
        ):
            result = authenticate_in_firebase('test_token')

        self.assertEqual(result, user_info)
        self.assertTrue(mock_get_user.called)

    @patch(
        'authentication.firebase_connector.auth.get_user',
    )
    def test_authenticate_in_firebase_with_anonymous_user_fails(
            self,
            mock_get_user,
    ):
        user_info = {
            'uid': 'test_uid',
            'firebase': {
                'sign_in_provider': 'anonymous'
            }
        }

        with patch(
                'authentication.firebase_connector.get_user_info_by_firebase_token',
                return_value=user_info
        ):
            with self.assertRaises(AuthenticationFailed):
                result = authenticate_in_firebase('test_token')

    @patch(
        'authentication.firebase_connector.auth.get_user',
    )
    @patch(
        'authentication.firebase_connector.firebase_auth_settings.EMAIL_VERIFICATION',
    )
    def test_authenticate_in_firebase_with_email_not_verified_fails(
            self,
            mock_email_verification,
            mock_get_user,
    ):
        user_info = {
            'uid': 'test_uid',
            'firebase': {
                'sign_in_provider': 'mail'
            }
        }
        mock_firebase_user = MagicMock()
        mock_firebase_user.email_verified = False
        mock_get_user.return_value = mock_firebase_user
        mock_email_verification = True

        with patch(
                'authentication.firebase_connector.get_user_info_by_firebase_token',
                return_value=user_info
        ):
            with self.assertRaises(AuthenticationFailed):
                result = authenticate_in_firebase('test_token')
