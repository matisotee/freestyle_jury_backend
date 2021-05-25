from unittest.mock import patch
import pytest

from competition.application.competition_creator import CompetitionCreator
from competition.application.exceptions import CompetitionApplicationError
from frimesh.client import FrimeshClient
from frimesh.exceptions import CallActionError, ServerError
from shared.frimesh_services_map import services_map


@pytest.mark.usefixtures("now_date")
@patch.object(CompetitionCreator, 'create_competition')
def test_create_competition(mock_creator, now_date):
    payload = {
        'name': 'test_competition_name',
        'date': now_date,
        'open_inscription_during_competition': True,
        'organizer': {
            'name': 'test_name',
            'last_name': 'test_last_name',
            'aka': 'test_aka',
            '_id': '1234'
        }
    }
    client = FrimeshClient(services_map)

    client.call('competition', 'create_competition', payload)

    mock_creator.assert_called()


@pytest.mark.usefixtures("now_date")
@patch.object(CompetitionCreator, 'create_competition')
def test_create_competition_with_error(mock_creator, now_date):
    mock_creator.side_effect = CompetitionApplicationError(
        message='test_message', code='TEST_CODE'
    )
    payload = {
        'name': 'test_competition_name',
        'date': now_date,
        'open_inscription_during_competition': True,
        'organizer': {
            'name': 'test_name',
            'last_name': 'test_last_name',
            'aka': 'test_aka',
            '_id': '1234'
        }
    }
    client = FrimeshClient(services_map)

    with pytest.raises(CallActionError) as ex_info:
        client.call('competition', 'create_competition', payload)

    exception = ex_info.value
    assert exception.code == 'TEST_CODE'


@pytest.mark.usefixtures("now_date")
def test_create_competition_with_request_schema_error(now_date):
    payload = {
        'name': 'test_competition_name',
        'date': now_date,
        'open_inscription_during_competition': True,
    }
    client = FrimeshClient(services_map)

    with pytest.raises(ServerError):
        client.call('competition', 'create_competition', payload)


