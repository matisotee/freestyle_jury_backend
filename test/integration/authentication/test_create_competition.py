import datetime
from unittest.mock import MagicMock

import pytest
import pytz

from rest_framework import status

from authentication.application.exceptions.services import CallServiceError
from authentication.dependency_injection import container


@pytest.fixture
def now_date():
    date_now = datetime.datetime.now(tz=datetime.timezone.utc).astimezone(
        pytz.timezone('America/Argentina/Buenos_Aires')
    )
    date_now_plus_an_hour = date_now + datetime.timedelta(hours=1)
    return date_now_plus_an_hour.isoformat()


@pytest.mark.django_db
@pytest.mark.usefixtures("authenticated_client")
def test_create_competition_successfully(authenticated_client, now_date):
    """Test create a new competition with valid payload is successful"""
    mock_service_caller = MagicMock()
    mock_service_caller.call.return_value = {'name': 'Rapublik', 'status': 'created'}

    payload = {
       'name': "Rapublik",
       'date': now_date,
       'open_inscription_during_competition': True
    }

    with container.service_caller.override(mock_service_caller):
        response = authenticated_client.post('/competitions/', payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
       'name': "Rapublik",
       'status': 'created'
    }
    mock_service_caller.call.assert_called()


@pytest.mark.django_db
@pytest.mark.usefixtures("authenticated_client")
def test_create_competition_without_name_fails(authenticated_client, now_date):

    payload = {
        'date': now_date,
        'open_inscription_during_competition': True
    }

    response = authenticated_client.post('/competitions/', payload)

    assert response.status_code == 400
    assert response.data['error_code'] == 'FIELDS_ERROR'


@pytest.mark.django_db
@pytest.mark.usefixtures("authenticated_client")
def test_create_competition_with_wrong_date_fails(authenticated_client):

    payload = {
        'name': "Rapublik",
        'date': 'test',
        'open_inscription_during_competition': True
    }

    response = authenticated_client.post('/competitions/', payload)

    assert response.status_code == 400
    assert response.data['error_code'] == 'FIELDS_ERROR'


@pytest.mark.django_db
@pytest.mark.usefixtures("authenticated_client")
def test_create_competition_with_service_exception(authenticated_client, now_date):
    mock_service_caller = MagicMock()
    mock_service_caller.call.side_effect = CallServiceError(message='Test', code='TEST_CODE')

    payload = {
        'name': "Rapublik",
        'date': now_date,
        'open_inscription_during_competition': True
    }

    with container.service_caller.override(mock_service_caller):
        response = authenticated_client.post('/competitions/', payload)

    assert response.status_code == 400
    assert response.data['error_code'] == 'TEST_CODE'
