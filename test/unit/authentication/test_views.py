from unittest.mock import patch, MagicMock

import pytest
from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from authentication.models import User
from authentication.views import RegisterUserView
from utils.feature_flags.clients import FeatureFlagManager


REGISTER_USER_URL = '/auth/register/'


@pytest.mark.usefixtures("client")
@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
@patch.object(User, 'objects')
def test_post_successfully(mock_objects, mock_ff, client):
    payload = {
        'name': 'Test Name',
        'last_name': 'Last Name',
        'aka': 'test',
        'token': 'test',
    }

    user = User(
        uid='test',
        name=payload['name'],
        last_name=payload['last_name'],
        aka=payload['aka']
    )
    mock_objects.create_user_by_token.return_value = user

    response = client.post(REGISTER_USER_URL, payload)

    assert isinstance(response, Response)
    assert response.data == {
        'name': 'Test Name',
        'last_name': 'Last Name',
        'aka': 'test',
    }
    assert response.status_code == status.HTTP_201_CREATED


@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
def test_post_with_non_valid_request(mock_ff):
    payload = {
        'name': 'Test Name',
    }

    view = RegisterUserView()
    request = MagicMock()
    request.data = payload

    with pytest.raises(ValidationError):
        view.post(request)


@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
@patch.object(User, 'objects')
def test_post_with_existent_user_in_request(mock_objects, mock_ff):
    mock_objects.create_user_by_token.side_effect = IntegrityError()
    payload = {
        'name': 'Test Name',
        'last_name': 'Last Name',
        'aka': 'test',
        'token': 'test',
    }
    view = RegisterUserView()
    request = MagicMock()
    request.data = payload

    with pytest.raises(ValidationError) as exc_info:
        view.post(request)
    exception_raised = exc_info.value
    assert exception_raised.detail[0].code == 'USER_ALREADY_EXIST'


@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=False)
def test_post_fail_with_ff_diabled(mock_ff):
    view = RegisterUserView()
    request = MagicMock()

    result = view.post(request)

    assert result.status_code == status.HTTP_401_UNAUTHORIZED
