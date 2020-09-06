from unittest.mock import patch

from django.test import TestCase
from rest_framework.exceptions import AuthenticationFailed

from authentication.authenticator import FirebaseAuthentication, User


class FirebaseAuthenticationTest(TestCase):

    def setUp(self):
        self.authenticator = FirebaseAuthentication()

    @patch.object(FirebaseAuthentication, 'get_user_by_uid', return_value='mock_user')
    @patch(
        'authentication.authenticator.authenticate_in_firebase',
        return_value={'uid': 'mock_uid'}
    )
    @patch.object(FirebaseAuthentication, 'get_token', return_value='token')
    def test_authenticate_successfully(self, mock_get_token, mock_firebase, mock_get_user):

        result = self.authenticator.authenticate('request')

        self.assertEqual(result, ('mock_user', {'uid': 'mock_uid'}))
        self.assertTrue(mock_get_token.called)
        self.assertTrue(mock_firebase.called)
        self.assertTrue(mock_get_user.called)

    @patch.object(FirebaseAuthentication, 'get_token', return_value=None)
    def test_authenticate_without_token(self, mock_get_token):
        result = self.authenticator.authenticate('request')

        self.assertIsNone(result)

    @patch(
        'authentication.authenticator.get_authorization_header',
        return_value='Bearer token'.encode()
    )
    def test_get_token_successfully(self, mock_get_token):

        result = self.authenticator.get_token('request')

        self.assertEqual(result, b'token')

    @patch(
        'authentication.authenticator.get_authorization_header',
        return_value=''
    )
    def test_get_token_without_authentication_header(self, mock_get_token):
        result = self.authenticator.get_token('request')

        self.assertIsNone(result)

    @patch(
        'authentication.authenticator.get_authorization_header',
        return_value='Bearer'.encode()
    )
    def test_get_token_without_token(self, mock_get_token):

        with self.assertRaises(AuthenticationFailed):
            self.authenticator.get_token('request')

    @patch(
        'authentication.authenticator.get_authorization_header',
        return_value='Bearer token space'.encode()
    )
    def test_get_token_with_spaced_token(self, mock_get_token):
        with self.assertRaises(AuthenticationFailed):
            self.authenticator.get_token('request')

    def test_get_user_by_uid_successfully(self):

        user = User.objects.create_user(uid='uid', name='test', last_name='user')

        result = self.authenticator.get_user_by_uid('uid')

        self.assertEqual(result, user)

    def test_get_user_by_uid_with_non_existent_user(self):

        with self.assertRaises(AuthenticationFailed):
            self.authenticator.get_user_by_uid('uid')

    def test_authenticate_header(self):

        result = self.authenticator.authenticate_header('request')

        expected = '{} realm="{}"'.format(
            self.authenticator.auth_header_prefix, self.authenticator.www_authenticate_realm
        )

        self.assertEqual(result, expected)
