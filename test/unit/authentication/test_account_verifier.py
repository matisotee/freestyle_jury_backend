from unittest.mock import patch, MagicMock

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.account_verifier import AccountVerifier
from authentication.mailer import UserMailer


class AccountVerifierTest(TestCase):

    def setUp(self):
        self.user_parameters = {
            'email': 'matias@test.com',
            'password': 'Testpass123',
            'name': 'matias',
            'last_name': 'perez',
            'aka': 'sot'
        }
        self.user = get_user_model().objects.create_user(**self.user_parameters)

    @patch.object(RefreshToken, 'for_user')
    @patch.object(UserMailer, 'send_verification_account_email')
    def test_generate_verification_token_successful(self, mock_send_email, mock_for_user):
        refresh_token = MagicMock()
        refresh_token.access_token = '1234'
        mock_for_user.return_value = refresh_token

        AccountVerifier.generate_verification_token_for_user(self.user)

        mock_send_email.assert_called_once_with(self.user, '1234')

    def test_generate_verification_token_for_user_verified_fails(self):
        self.user.is_verified = True

        with self.assertRaises(ValidationError):
            AccountVerifier.generate_verification_token_for_user(self.user)
