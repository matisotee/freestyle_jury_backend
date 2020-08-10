from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from authentication.mailer import UserMailer


class MailerTest(TestCase):

    def setUp(self):
        self.user_parameters = {
            'email': 'matias@test.com',
            'password': 'Testpass123',
            'name': 'matias',
            'last_name': 'perez',
            'aka': 'sot'
        }
        self.user = get_user_model().objects.create_user(**self.user_parameters)

    @patch('authentication.mailer.send_mail')
    def test_send_verification_mail(self, mock_send_mail):
        token = '1234'
        url = f'http://wwww.{settings.FRONTEND_DOMAIN}{UserMailer.EMAIL_VERIFICATION_URL}?token={token}'

        UserMailer().send_verification_account_email(self.user, token)

        mock_send_mail.assert_called_once_with(
            subject=UserMailer.EMAIL_VERIFICATION_SUBJECT,
            message='Hola matias,\n Utiliza el siguiente link para verificar tu cuenta\n{}'.format(url),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user_parameters['email'], ]
        )
