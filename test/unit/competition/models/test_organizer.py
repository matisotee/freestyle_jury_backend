import datetime
from unittest.mock import patch, MagicMock

import pytest
from django.core.exceptions import ValidationError
from djongo.sql2mongo import SQLDecodeError

from competition.models.competition import Competition
from competition.models.organizer import Organizer


@patch.object(Organizer, 'save')
def test_create_successfully(mock_save):

    organizer_dict = {
        'uid': '1234',
        'name': 'Test',
        'last_name': 'test',
        'aka': 't'
    }

    organizer = Organizer.objects.create(**organizer_dict)

    assert isinstance(organizer, Organizer)
    assert organizer.uid == '1234'
    assert organizer.name == 'Test'
    assert organizer.last_name == 'test'
    assert organizer.aka == 't'
    assert organizer.competitions.count() == 0


def test_create_without_name_fails():

    organizer_dict = {
        'uid': '1234',
        'last_name': 'test',
        'aka': 't'
    }

    with pytest.raises(ValidationError):
        Organizer.objects.create(**organizer_dict)


@patch.object(Organizer, 'save')
def test_create_with_db_constraint_error_fails(mock_save):
    organizer_dict = {
        'uid': '1234',
        'name': 'Test',
        'last_name': 'test',
        'aka': 't'
    }
    mock_save.side_effect = SQLDecodeError(err_sql='duplicate key error collection')

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
    organizer = Organizer(uid='123', name='Test', last_name='test', aka='t')

    result = organizer.create_competition('Test', date_now, True)

    assert result == competition
    mock_competitions.add.assert_called_with(competition)

