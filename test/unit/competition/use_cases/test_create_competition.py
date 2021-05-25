import datetime
from unittest.mock import patch

import pytest
import pytz

from competition.application.competition_creator import CompetitionCreator
from competition.application.exceptions import CompetitionApplicationError
from competition.domain.models.competition import Competition
from competition.domain.models.organizer import Organizer, OrganizerManager
from test.utils import generate_object_id


@pytest.fixture
def user_dict():
    return {
        'name': 'Test',
        'last_name': 'Test',
        'aka': 'T',
        '_id': generate_object_id(),
    }


@pytest.fixture
def competition():
    date = datetime.datetime.now().astimezone(
        pytz.timezone('Etc/GMT+3')
    ) + datetime.timedelta(hours=1)
    return Competition(
        name='Rapublik',
        date=date,
        open_inscription_during_competition=True,
        status='created'
    )


@patch.object(Competition, 'save')
@patch.object(Organizer, 'save')
@patch.object(Organizer, 'competitions')
@patch.object(OrganizerManager, 'get')
def test_create_competition_with_existent_organizer_successfully(
    mock_organizer_get,
    mock_organizer_competitions,
    mock_save_organizer,
    mock_save_competition,
    user_dict,
    competition
):

    mock_organizer_get.return_value = Organizer(**user_dict)

    result = CompetitionCreator.create_competition(
        user_dict,
        competition.name,
        competition.date,
        competition.open_inscription_during_competition
    )

    assert result == {
        'name': competition.name,
        'status': competition.status
    }
    mock_save_organizer.assert_not_called()
    mock_save_competition.assert_called()
    mock_organizer_competitions.add.assert_called()


@patch.object(Competition, 'save')
@patch.object(Organizer, 'competitions')
@patch.object(Organizer, 'save')
@patch.object(Organizer, 'full_clean')
@patch.object(OrganizerManager, 'get')
def test_create_competition_with_nonexistent_organizer_successfully(
    mock_organizer_get,
    mock_full_clean,
    mock_organizer_save,
    mock_organizer_competitions,
    mock_competition_save,
    user_dict,
    competition
):

    mock_organizer_get.side_effect = Organizer.DoesNotExist()

    result = CompetitionCreator.create_competition(
        user_dict,
        competition.name,
        competition.date,
        competition.open_inscription_during_competition
    )

    assert result == {
        'name': competition.name,
        'status': competition.status
    }
    mock_full_clean.assert_called()
    mock_organizer_save.assert_called()
    mock_organizer_competitions.add.assert_called()
    mock_competition_save.assert_called()


@patch.object(OrganizerManager, 'get')
def test_create_competition_past_date_fails(
    mock_organizer_get,
    user_dict,
    competition
):
    mock_organizer_get.return_value = Organizer(**user_dict)
    past_date = datetime.datetime.now().astimezone(
        pytz.timezone('Etc/GMT+3')
    ) - datetime.timedelta(hours=1)

    with pytest.raises(CompetitionApplicationError) as ex_info:
        CompetitionCreator.create_competition(
            user_dict,
            competition.name,
            past_date,
            competition.open_inscription_during_competition
        )
    exception = ex_info.value
    assert exception.code == 'PAST_DATE'
