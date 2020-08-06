from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('authentication:create_user')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class CreateUserApiTest(TestCase):
    """Test the users api public"""
    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'email': 'test@test.com',
            'password': 'testpass',
            'name': 'Test Name',
            'last_name': 'Last Name',
            'aka': 'sot'
        }

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        response = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertNotIn(self.payload['password'], response.data)

    def test_user_exist(self):
        """Test creating user that already exists fails"""
        create_user(**self.payload)

        response = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email(self):
        """Test creating user that already exists fails"""
        self.payload['email'] = ['abcd']
        response1 = self.client.post(CREATE_USER_URL, self.payload)

        self.payload['email'] = 'abcd'
        response2 = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        self.payload['password'] = 'pw'

        response = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=self.payload['email']
        ).exists()
        self.assertFalse(user_exist)
