from unittest.mock import patch
import pytest

from api_gateway.application.exceptions.registration import RegistrationError
from api_gateway.application.register_user import UserRegistrar
from api_gateway.infrastructure.controllers.base import ResponseError
from utils.feature_flags.clients import FeatureFlagManager


@pytest.mark.usefixtures("client")
@patch.object(UserRegistrar, 'register_user')
@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
def test_register_user_successfully(mock_ff, mock_register_user, client):
    """Test register user with valid payload is successful"""
    mock_register_user.return_value = {
        'id': '1234',
        'name': 'test_name',
        'last_name': 'test_last_name',
        'email': 'test@test.com',
        'phone_number': '',
        'aka': 'test_aka'
    }
    payload = {
        'name': 'Test Name',
        'last_name': 'Last Name',
        'aka': 'test',
        'token': 'test_token',
    }

    response = client.post('/auth/register/', payload, format='json')

    assert response.status_code == 200
    assert response.data == {
        'id': '1234',
        'name': 'test_name',
        'last_name': 'test_last_name',
        'email': 'test@test.com',
        'phone_number': '',
        'aka': 'test_aka'
    }


@pytest.mark.usefixtures("client")
@patch.object(UserRegistrar, 'register_user')
@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
def test_register_user_with_registration_error(mock_ff, mock_register_user, client):
    mock_register_user.side_effect = RegistrationError('test_error', 'TEST_CODE')
    payload = {
        'name': 'Test Name',
        'last_name': 'Last Name',
        'aka': 'test',
        'token': 'test_token',
    }

    response = client.post('/auth/register/', payload, format='json')

    assert response.status_code == 400
    assert response.data['error_code'] == 'TEST_CODE'


@pytest.mark.usefixtures("client")
@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
def test_register_user_with_request_schema_error(mock_ff, client):
    payload = {
        'name': 'Test Name',
        'last_name': 'Last Name',
        'aka': 'test',
    }

    response = client.post('/auth/register/', payload, format='json')

    assert response.status_code == 400
    assert response.data['error_code'] == 'FIELDS_ERROR'


@pytest.mark.usefixtures("client")
@patch.object(UserRegistrar, 'register_user')
@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
def test_register_user_with_response_schema_error(mock_ff, mock_register_user, client):
    mock_register_user.return_value = {
        'last_name': 'test_last_name',
        'aka': 'test_aka'
    }
    payload = {
        'name': 'Test Name',
        'last_name': 'Last Name',
        'aka': 'test',
        'token': 'test_token',
    }

    with pytest.raises(ResponseError):
        client.post('/auth/register/', payload, format='json')
