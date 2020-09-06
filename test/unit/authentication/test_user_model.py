from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from authentication.models import User, UserManager


class UserModelTests(TestCase):

    def setUp(self):
        self.user_parameters = {
            'uid': 'test_uid',
            'name': 'matias',
            'last_name': 'perez',
            'aka': 'sot'
        }

    def test_create_user_successful(self):
        """Test creating a new user successfully"""
        user = get_user_model().objects.create_user(**self.user_parameters)

        for key, value in self.user_parameters.items():
            self.assertEqual(getattr(user, key), value)

    def test_create_user_without_name_fails(self):
        """Test creating a new user with an email is successful"""
        self.user_parameters['name'] = ''

        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(**self.user_parameters)
        with self.assertRaises(User.DoesNotExist):
            self.assertIsNone(get_user_model().objects.get(aka=self.user_parameters['aka']))

    def test_create_existent_user_fails(self):
        """Test creating user with invalid email raises error"""
        get_user_model().objects.create_user(**self.user_parameters)

        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(**self.user_parameters)

    @patch(
        'authentication.models.get_user_info_by_firebase_token',
        return_value={'uid': 'test_uid'}
    )
    @patch.object(UserManager, 'create_user')
    def test_create_user_by_token(self, mock_create, mock_firebase):
        """Test creating user with invalid email raises error"""
        self.user_parameters.pop('uid')
        self.user_parameters['token'] = 'test_token'

        get_user_model().objects.create_user_by_token(**self.user_parameters)
        self.assertTrue(mock_firebase.called)
        self.assertTrue(mock_create.called)
        self.assertEqual(mock_create.call_args[0], ('test_uid', 'matias', 'perez', 'sot'))

    def test_create_new_super_user(self):
        """Test creating a new super user"""
        user = get_user_model().objects.create_superuser('test')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
