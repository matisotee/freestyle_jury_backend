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
    def test_start_verification_account_process_successful(self, mock_send_email, mock_for_user):
        refresh_token = MagicMock()
        refresh_token.access_token = '1234'
        mock_for_user.return_value = refresh_token

        AccountVerifier.start_verification_account_process(self.user.email)

        mock_send_email.assert_called_once_with(self.user, '1234')

    def test_start_verification_account_process_for_user_verified_fails(self):
        self.user.is_verified = True
        self.user.save()

        with self.assertRaises(ValidationError):
            AccountVerifier.start_verification_account_process(self.user.email)

    def test_start_verification_account_process_with_nonexistent_email_fail(self):

        with self.assertRaises(ValidationError):
            AccountVerifier.start_verification_account_process('test@gmail.com')
