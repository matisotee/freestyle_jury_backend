from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from firebase_admin import auth

from authentication.firebase_connector import FirebaseConnector
from authentication.models import User, UserManager
from utils.feature_flags.clients import FeatureFlagManager

REGISTER_USER_URL = reverse('authentication:register_user')


def create_user(**kwargs):
    return User.objects.create_user(**kwargs)


# Test the users api public
@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def end_point_payload():
    return {
        'token': 'test_token',
        'name': 'Test Name',
        'last_name': 'Last Name',
        'aka': 'test'
    }


@pytest.fixture
def end_point_payload_without_name():
    return {
        'token': 'test_token',
        'last_name': 'Last Name',
        'aka': 'test'
    }


@pytest.fixture
def user_payload():
    return {
        'uid': 'test_uid',
        'name': 'Test Name',
        'last_name': 'Last Name',
        'aka': 'test'
    }


@patch.object(UserManager, 'filter')
@patch.object(User, 'save')
@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
@patch(
    'authentication.firebase_connector.auth.verify_id_token',
    return_value={'uid': 'test_uid'}
)
def test_register_user_successfully(
        mock_firebase, mock_ff, mock_save, mock_filter, client, end_point_payload
):
    """Test register user with valid payload is successful"""
    mock_filter.return_value.exists.return_value = False
    FirebaseConnector.is_initialized = True

    response = client.post(REGISTER_USER_URL, end_point_payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert end_point_payload['token'] not in response.data


@patch.object(UserManager, 'filter')
@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
@patch(
    'authentication.firebase_connector.auth.verify_id_token',
    return_value={'uid': 'test_uid'}
)
def test_register_existent_user_fails(
        mock_firebase, mock_ff, mock_filter, client, end_point_payload
):
    """Test register user that already exists fails"""
    mock_filter.return_value.exists.return_value = True
    FirebaseConnector.is_initialized = True

    response = client.post(REGISTER_USER_URL, end_point_payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
@patch(
    'authentication.firebase_connector.auth.verify_id_token',
    side_effect=auth.InvalidIdTokenError('Invalid')
)
def test_register_user_with_invalid_token(mock_firebase, mock_ff, client, end_point_payload):
    """Test register an user with an invalid firebase token"""
    FirebaseConnector.is_initialized = True
    response = client.post(REGISTER_USER_URL, end_point_payload)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@patch.object(UserManager, 'filter')
@patch(
    'authentication.firebase_connector.auth.verify_id_token',
    return_value={'uid': 'test_uid'}
)
@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
def test_register_user_without_name(
        mock_ff, mock_verify_id_token, mock_filter, end_point_payload_without_name, client
):
    """Test register an user without name"""
    mock_filter.return_value.exists.return_value = False

    response = client.post(REGISTER_USER_URL, end_point_payload_without_name)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
