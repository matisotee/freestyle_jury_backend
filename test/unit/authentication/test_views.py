from unittest.mock import patch, MagicMock

from django.db import IntegrityError
from django.test import TestCase
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from authentication.serializers import RegisterUserSerializer
from authentication.views import RegisterUserView
from utils.feature_flags.clients import FeatureFlagManager


class RegisterUserViewTest(TestCase):

    @patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
    @patch.object(RegisterUserSerializer, '__init__', return_value=None)
    @patch.object(RegisterUserSerializer, 'is_valid', return_value=True)
    @patch.object(RegisterUserSerializer, 'data')
    def test_post_successfully(self, mock_data, mock_is_valid, mock_init, mock_ff):
        view = RegisterUserView()
        request = MagicMock()
        request.data = 'data'

        result = view.post(request)

        self.assertIsInstance(result, Response)
        self.assertEqual(result.data, mock_data)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    @patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
    @patch.object(RegisterUserSerializer, '__init__', return_value=None)
    @patch.object(RegisterUserSerializer, 'is_valid', return_value=False)
    def test_post_with_non_valid_request(self, mock_is_valid, mock_init, mock_ff):
        view = RegisterUserView()
        request = MagicMock()
        request.data = 'data'

        with self.assertRaises(ValidationError):
            view.post(request)

    @patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
    @patch.object(RegisterUserSerializer, '__init__', return_value=None)
    @patch.object(RegisterUserSerializer, 'is_valid', side_effect=IntegrityError())
    def test_post_with_existent_user_in_request(self, mock_is_valid, mock_init, mock_ff):
        view = RegisterUserView()
        request = MagicMock()
        request.data = 'data'

        with self.assertRaises(ValidationError):
            view.post(request)

    @patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=False)
    def test_post_fail_with_ff_diabled(self, mock_ff):
        view = RegisterUserView()
        request = MagicMock()

        result = view.post(request)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)
