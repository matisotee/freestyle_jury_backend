from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from firebase_admin import auth


REGISTER_USER_URL = reverse('authentication:register_user')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class CreateUserApiTest(TestCase):
    """Test the users api public"""
    def setUp(self):
        self.client = APIClient()
        self.end_point_payload = {
            'token': 'test_token',
            'name': 'Test Name',
            'last_name': 'Last Name',
            'aka': 'test'
        }
        self.user_payload = {
            'uid': 'test_uid',
            'name': 'Test Name',
            'last_name': 'Last Name',
            'aka': 'test'
        }

    @patch('authentication.firebase_connector.is_initialized')
    @patch(
        'authentication.firebase_connector.auth.verify_id_token',
        return_value={'uid': 'test_uid'}
    )
    def test_register_user_successfully(self, mock_firebase, mock_is_initialized):
        """Test register user with valid payload is successful"""
        mock_is_initialized = True
        response = self.client.post(REGISTER_USER_URL, self.end_point_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(get_user_model().objects.filter(uid='test_uid').exists())
        self.assertNotIn(self.end_point_payload['token'], response.data)

    @patch('authentication.firebase_connector.is_initialized')
    @patch(
        'authentication.firebase_connector.auth.verify_id_token',
        return_value={'uid': 'test_uid'}
    )
    def test_register_existent_user_fails(self, mock_firebase, mock_is_initialized):
        """Test register user that already exists fails"""
        mock_is_initialized = True
        create_user(**self.user_payload)

        response = self.client.post(REGISTER_USER_URL, self.end_point_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('authentication.firebase_connector.is_initialized')
    @patch(
        'authentication.firebase_connector.auth.verify_id_token',
        side_effect=auth.InvalidIdTokenError('Invalid')
    )
    def test_register_user_with_invalid_token(self, mock_firebase, mock_is_initialized):
        """Test register an user with an invalid firebase token"""
        mock_is_initialized = True
        response = self.client.post(REGISTER_USER_URL, self.end_point_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_register_user_without_name(self):
        """Test register an user without name"""
        self.end_point_payload.pop('name')
        response = self.client.post(REGISTER_USER_URL, self.end_point_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
