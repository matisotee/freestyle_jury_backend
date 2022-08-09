from unittest.mock import patch
import pytest

from api_gateway.domain.models import User
from shared.feature_flags import FeatureFlagManager

REGISTER_USER_URL = '/users/'


@pytest.mark.django_db
@pytest.mark.usefixtures("client")
@pytest.mark.usefixtures("firebase_user")
@patch.object(FeatureFlagManager, 'is_feature_enabled', return_value=True)
def test_register_user_successfully(mock_ff, firebase_user, client):
    """Test register user with valid payload is successful"""
    payload = {
        'name': 'Test Name',
        'last_name': 'Last Name',
        'aka': 'test',
        'token': firebase_user.token,
    }

    response = client.post(REGISTER_USER_URL, payload, format='json')

    assert response.status_code == 200
    assert response.data['id'] is not None
    assert response.data['name'] == 'Test Name'
    assert response.data['last_name'] == 'Last Name'
    assert response.data['email'] == firebase_user.email
    assert response.data['aka'] == 'test'
    assert payload['token'] not in response.data
