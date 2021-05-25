from unittest.mock import patch
import pytest
from rest_framework import status

from api_gateway.application.create_competition import CreateCompetitionService
from api_gateway.application.exceptions.competition import CreateCompetitionError
from api_gateway.infrastructure.controllers.base import ResponseError


@pytest.mark.usefixtures("now_date")
@pytest.mark.usefixtures("mock_authenticated_client")
@patch.object(CreateCompetitionService, 'create_competition')
def test_create_competition_successfully(
        mock_create_competition, mock_authenticated_client, now_date
):
    expected_response = {
       'name': "Rapublik",
       'status': 'created'
    }
    mock_create_competition.return_value = expected_response

    payload = {
       'name': "Rapublik",
       'date': now_date,
       'open_inscription_during_competition': True
    }

    response = mock_authenticated_client.post('/competitions/', payload, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_response
    mock_create_competition.assert_called()


@pytest.mark.usefixtures("now_date")
@pytest.mark.usefixtures("mock_authenticated_client")
@patch.object(CreateCompetitionService, 'create_competition')
def test_create_competition_with_error(
        mock_create_competition, mock_authenticated_client, now_date
):
    mock_create_competition.side_effect = CreateCompetitionError(
        message='Test', code='TEST_CODE'
    )

    payload = {
       'name': "Rapublik",
       'date': now_date,
       'open_inscription_during_competition': True
    }

    response = mock_authenticated_client.post('/competitions/', payload, format='json')

    assert response.status_code == 400
    assert response.data['error_code'] == 'TEST_CODE'
    mock_create_competition.assert_called()


@pytest.mark.usefixtures("now_date")
@pytest.mark.usefixtures("mock_authenticated_client")
def test_create_competition_with_request_schema_error(
        mock_authenticated_client, now_date
):
    payload = {
       'date': now_date,
       'open_inscription_during_competition': True
    }

    response = mock_authenticated_client.post('/competitions/', payload, format='json')

    assert response.status_code == 400
    assert response.data['error_code'] == 'FIELDS_ERROR'


@pytest.mark.usefixtures("now_date")
@pytest.mark.usefixtures("mock_authenticated_client")
@patch.object(CreateCompetitionService, 'create_competition')
def test_create_competition_with_response_schema_error(
        mock_create_competition, mock_authenticated_client, now_date
):
    mock_create_competition.return_value = {
       'status': 'created'
    }

    payload = {
       'name': "Rapublik",
       'date': now_date,
       'open_inscription_during_competition': True
    }

    with pytest.raises(ResponseError):
        mock_authenticated_client.post('/competitions/', payload, format='json')
