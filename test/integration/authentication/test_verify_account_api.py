from unittest.mock import patch, MagicMock

import jwt
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

VERIFY_ACCOUNT_URL = reverse('authentication:verify_account')


class VerifyAccountApiTest(TestCase):

    @patch('authentication.account_verifier.jwt.decode')
    @patch('authentication.account_verifier.get_user_model')
    def test_verify_account_success(self, mock_user_model, mock_decode):
        user = MagicMock()
        user.is_verified = False
        user.save = MagicMock()
        model = MagicMock()
        model.objects.get = MagicMock(return_value=user)
        mock_user_model.return_value = model

        response = self.client.get(VERIFY_ACCOUNT_URL, {'token': 'token'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('authentication.account_verifier.jwt.decode', side_effect=jwt.exceptions.ExpiredSignatureError)
    def test_verify_account_token_expired(self, mock_decode):

        response = self.client.get(VERIFY_ACCOUNT_URL, {'token': 'token'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].code, 'TOKEN_EXPIRED')

    @patch('authentication.account_verifier.jwt.decode', side_effect=jwt.exceptions.DecodeError)
    def test_verify_account_token_invalid(self, mock_decode):
        response = self.client.get(VERIFY_ACCOUNT_URL, {'token': 'token'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].code, 'TOKEN_INVALID')
