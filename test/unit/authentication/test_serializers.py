from unittest.mock import patch

from django.test import TestCase
from authentication.serializers import RegisterUserSerializer


class RegisterUserSerializerTest(TestCase):

    @patch('authentication.serializers.Serializer.validate')
    @patch('authentication.serializers.get_user_model')
    def test_validate(self, mock_get_user_model, mock_validate):

        payload = {
            'name': 'test',
            'last_name': 'user',
            'aka': 'aka',
            'token': 'token'
        }
        mock_validate.return_value = payload
        serializer = RegisterUserSerializer()

        serializer.validate(payload)

        self.assertTrue(mock_validate.called)
        mock_get_user_model().objects.create_user_by_token.assert_called_with(
            name='test', last_name='user', token='token', aka='aka'
        )
