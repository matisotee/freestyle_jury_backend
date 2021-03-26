import datetime
from unittest.mock import patch

import pytest
import pytz

from competition.exceptions import OrganizerCreationError
from competition.models.competition import Competition
from competition.models.organizer import Organizer
from competition.services.competition_creator import CompetitionCreator
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
    ).isoformat()
    return Competition(
        name='Rapublik',
        date=date,
        open_inscription_during_competition=True,
        status='created'
    )


@patch.object(Organizer, 'create_competition')
@patch.object(Organizer, 'objects')
def test_create_competition_with_existent_organizer_successfully(
    mock_organizer_objects,
    mock_create_competition,
    user_dict,
    competition
):

    mock_organizer_objects.get.return_value = Organizer(**user_dict)

    mock_create_competition.return_value = competition

    result = CompetitionCreator.create_competition(
        user_dict,
        competition.name,
        competition.date,
        competition.open_inscription_during_competition
    )

    assert result == competition


@patch.object(Organizer, 'create_competition')
@patch.object(Organizer, 'objects')
def test_create_competition_with_nonexistent_organizer_successfully(
    mock_organizer_objects,
    mock_create_competition,
    user_dict,
    competition
):

    mock_organizer_objects.get.side_effect = Organizer.DoesNotExist()
    mock_organizer_objects.create.return_value = Organizer(**user_dict)

    mock_create_competition.return_value = competition

    result = CompetitionCreator.create_competition(
        user_dict,
        competition.name,
        competition.date,
        competition.open_inscription_during_competition
    )

    assert result == competition


def test_create_competition_organizer_without_uid_fails(competition):
    user_dict = {
        'name': 'Test',
        'last_name': 'Test',
        'aka': 'T',
    }

    with pytest.raises(OrganizerCreationError):
        CompetitionCreator.create_competition(
            user_dict,
            competition.name,
            competition.date,
            competition.open_inscription_during_competition
        )
