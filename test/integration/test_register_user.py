from unittest.mock import patch
import pytest

from api_gateway.infrastructure.repositories.user_repository import MongoUserRepository
from shared.feature_flags import FeatureFlagManager


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

    response = client.post('/users/', json=payload)

    assert response.status_code == 200
    assert response.json()['id'] is not None
    assert response.json()['name'] == 'Test Name'
    assert response.json()['last_name'] == 'Last Name'
    assert response.json()['email'] == firebase_user.email
    assert response.json()['aka'] == 'test'
    assert payload['token'] not in response.json()

    repository = MongoUserRepository()
    repository.delete(response.json()['id'])
