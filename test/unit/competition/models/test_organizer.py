import datetime
from unittest.mock import patch

import pytest
from django.core.exceptions import ValidationError

from competition.models.competition import Competition
from competition.models.organizer import Organizer, OrganizerManager
from test.utils import generate_object_id


@patch.object(OrganizerManager, 'filter')
@patch.object(Organizer, 'save')
def test_create_successfully(mock_save, mock_filter):

    organizer_id = generate_object_id()

    organizer_dict = {
        '_id': organizer_id,
        'name': 'Test',
        'last_name': 'test',
        'aka': 't'
    }
    mock_filter.return_value.exists.return_value = False

    organizer = Organizer.objects.create(**organizer_dict)

    assert isinstance(organizer, Organizer)
    assert str(organizer._id) == organizer_id
    assert organizer.name == 'Test'
    assert organizer.last_name == 'test'
    assert organizer.aka == 't'
    assert organizer.competitions.count() == 0


@patch.object(OrganizerManager, 'filter')
def test_create_with_empty_name(mock_filter):
    organizer_dict = {
        '_id': generate_object_id(),
        'name': '',
        'last_name': 'test',
        'aka': 't'
    }
    mock_filter.return_value.exists.return_value = False

    with pytest.raises(ValidationError):
        Organizer.objects.create(**organizer_dict)


@patch.object(OrganizerManager, 'filter')
def test_create_already_existent_organizer(mock_filter):
    organizer_dict = {
        '_id': generate_object_id(),
        'name': 'Test',
        'last_name': 'test',
        'aka': 't'
    }
    mock_filter.return_value.exists.return_value = True

    with pytest.raises(ValidationError):
        Organizer.objects.create(**organizer_dict)


@patch.object(Competition, 'objects')
@patch.object(Organizer, 'competitions')
def test_create_competition(mock_competitions, mock_competition_objects):
    date_now = datetime.datetime.now(tz=datetime.timezone.utc)
    competition = Competition(
        name='Test',
        date=date_now,
        open_inscription_during_competition=True
    )
    mock_competition_objects.create.return_value = competition
    organizer = Organizer(_id='123', name='Test', last_name='test', aka='t')

    result = organizer.create_competition('Test', date_now, True)

    assert result == competition
    mock_competitions.add.assert_called_with(competition)

