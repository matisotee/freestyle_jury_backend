from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from authentication.models import User


class ModelTests(TestCase):

    def setUp(self):
        self.user_parameters = {
            'email': 'matias@test.com',
            'password': 'Testpass123',
            'name': 'matias',
            'last_name': 'perez',
            'aka': 'sot'
        }

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""

        user = get_user_model().objects.create_user(**self.user_parameters)

        self.assertTrue(user.check_password(self.user_parameters['password']))

        self.user_parameters.pop('password', None)
        self.user_parameters['is_verified'] = False

        for key, value in self.user_parameters.items():
            self.assertEqual(getattr(user, key), value)

    def test_create_user_without_name_fails(self):
        """Test creating a new user with an email is successful"""
        email = 'matias@test.com'
        password = 'Testpass123'

        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                email=email,
                password=password
            )
        with self.assertRaises(User.DoesNotExist):
            self.assertIsNone(get_user_model().objects.get(name=self.user_parameters['name']))

    def test_new_user_email_normalized(self):
        """Test the email for the new user is normalized"""
        self.user_parameters['email'] = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(**self.user_parameters)

        self.assertEqual(user.email, self.user_parameters['email'].lower())

    def test_new_user_invalid_email(self):
        """Test creating user with invalid email raises error"""
        self.user_parameters['email'] = ['test@test.com']

        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(**self.user_parameters)
        with self.assertRaises(User.DoesNotExist):
            self.assertIsNone(get_user_model().objects.get(name=self.user_parameters['name']))

    def test_create_new_super_user(self):
        """Test creating a new super user"""
        user = get_user_model().objects.create_superuser('email@test.com', '1234')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_verified)
