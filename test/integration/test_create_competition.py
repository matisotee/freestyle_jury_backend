import pytest
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.usefixtures("now_date")
@pytest.mark.usefixtures("authenticated_client")
def test_create_competition_successfully(authenticated_client, now_date):
    """Test create a new competition with valid payload is successful"""
    payload = {
       'name': "Rapublik",
       'date': now_date,
       'open_inscription_during_competition': True
    }

    response = authenticated_client.post('/competitions/', payload, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
       'name': "Rapublik",
       'status': 'created'
    }
