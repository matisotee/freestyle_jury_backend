from unittest.mock import patch, MagicMock

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.mailer import UserMailer

SEND_VERIFICATION_EMAIL_URL = reverse('authentication:verification_email')


class VerificationEmailApiTest(TestCase):
    """Test the users api public"""
    def setUp(self):
        self.client = APIClient()
        self.user_params = {
            'email': 'test@test.com',
            'password': 'testpass',
            'name': 'Test Name',
            'last_name': 'Last Name',
            'aka': 'sot'
        }
        self.user = get_user_model().objects.create_user(**self.user_params)
        self.payload = {'email': 'test@test.com'}

    @patch('authentication.mailer.send_mail')
    @patch.object(RefreshToken, 'for_user')
    def test_send_verification_email_success(self, mock_for_user, mock_send_email):
        """Test creating user with valid payload is successful"""
        refresh_token = MagicMock()
        refresh_token.access_token = '1234'
        mock_for_user.return_value = refresh_token
        url = f'http://wwww.{settings.FRONTEND_DOMAIN}{UserMailer.EMAIL_VERIFICATION_URL}?token={refresh_token.access_token}'

        response = self.client.post(SEND_VERIFICATION_EMAIL_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_send_email.assert_called_once_with(
            subject=UserMailer.EMAIL_VERIFICATION_SUBJECT,
            message='Hola Test Name,\n Utiliza el siguiente link para verificar tu cuenta\n{}'.format(url),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user_params['email'], ]
        )

    def test_send_verification_email_to_verified_user_fails(self):
        self.user.is_verified = True
        self.user.save()

        response = self.client.post(SEND_VERIFICATION_EMAIL_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].code, 'USER_VERIFIED')

    def test_send_verification_email_with_nonexistent_email(self):
        self.payload['email'] = 'invalid@email.com'

        response = self.client.post(SEND_VERIFICATION_EMAIL_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].code, 'EMAIL_INVALID')
        self.assertEqual(response.data[0], 'The email does not belong to a user')

    def test_send_verification_email_with_invalid_email(self):
        self.payload['email'] = 'invalid'

        response = self.client.post(SEND_VERIFICATION_EMAIL_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].code, 'EMAIL_INVALID')
        self.assertEqual(response.data[0], 'The field provided is not an email')
