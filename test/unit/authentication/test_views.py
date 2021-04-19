from unittest.mock import patch

import pytest
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response

from authentication.models import User
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


@pytest.mark.usefixtures("client")
@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
def test_post_with_non_valid_request(mock_ff, client):
    payload = {
        'name': 'Test Name',
    }

    response = client.post(REGISTER_USER_URL, payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error_code'] == 'FIELDS_ERROR'


@pytest.mark.usefixtures("client")
@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
@patch.object(User, 'objects')
def test_post_with_existent_user_in_request(mock_objects, mock_ff, client):
    mock_objects.create_user_by_token.side_effect = IntegrityError()
    payload = {
        'name': 'Test Name',
        'last_name': 'Last Name',
        'aka': 'test',
        'token': 'test',
    }

    response = client.post(REGISTER_USER_URL, payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error_code'] == 'USER_ALREADY_EXIST'
