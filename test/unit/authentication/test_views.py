from unittest.mock import patch, MagicMock

import pytest
from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from authentication.serializers import RegisterUserSerializer
from authentication.views import RegisterUserView
from utils.feature_flags.clients import FeatureFlagManager


@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
@patch.object(RegisterUserSerializer, '__init__', return_value=None)
@patch.object(RegisterUserSerializer, 'is_valid', return_value=True)
@patch.object(RegisterUserSerializer, 'data')
def test_post_successfully(mock_data, mock_is_valid, mock_init, mock_ff):
    view = RegisterUserView()
    request = MagicMock()
    request.data = 'data'

    result = view.post(request)

    assert isinstance(result, Response)
    assert result.data == mock_data
    assert result.status_code == status.HTTP_201_CREATED


@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
@patch.object(RegisterUserSerializer, '__init__', return_value=None)
@patch.object(RegisterUserSerializer, 'is_valid', return_value=False)
def test_post_with_non_valid_request(mock_is_valid, mock_init, mock_ff):
    view = RegisterUserView()
    request = MagicMock()
    request.data = 'data'

    with pytest.raises(ValidationError):
        view.post(request)


@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
@patch.object(RegisterUserSerializer, '__init__', return_value=None)
@patch.object(RegisterUserSerializer, 'is_valid', side_effect=IntegrityError())
def test_post_with_existent_user_in_request(mock_is_valid, mock_init, mock_ff):
    view = RegisterUserView()
    request = MagicMock()
    request.data = 'data'

    with pytest.raises(ValidationError):
        view.post(request)


@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=False)
def test_post_fail_with_ff_diabled(mock_ff):
    view = RegisterUserView()
    request = MagicMock()

    result = view.post(request)

    assert result.status_code == status.HTTP_401_UNAUTHORIZED
