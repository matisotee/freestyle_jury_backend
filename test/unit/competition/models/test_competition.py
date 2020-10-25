import datetime
from unittest.mock import patch

import pytest
import pytz
from django.core.exceptions import ValidationError

from competition.exceptions import CompetitionPastDateError, CompetitionCreationError
from competition.models.competition import Competition


@patch.object(Competition, 'save')
def test_create_successfully(mock_save):
    date_now = datetime.datetime.now().astimezone(
        pytz.timezone('Etc/GMT+3')
    )
    date_now_plus_an_hour = date_now + datetime.timedelta(hours=1)
    competition_dict = {
        'name': 'Test',
        'date': date_now_plus_an_hour,
        'open_inscription_during_competition': True
    }

    competition = Competition.objects.create(**competition_dict)

    assert isinstance(competition, Competition)
    assert competition.name == 'Test'
    assert competition.date == date_now_plus_an_hour
    assert competition.open_inscription_during_competition is True
    assert competition.status == 'created'


def test_create_without_name_fails():
    date_now = datetime.datetime.now(tz=datetime.timezone.utc)
    date_now_plus_an_hour = date_now + datetime.timedelta(hours=1)
    competition_dict = {
        'date': date_now_plus_an_hour,
        'open_inscription_during_competition': True
    }

    with pytest.raises(ValidationError):
        Competition.objects.create(**competition_dict)


def test_create_with_a_phase_fails():
    date_now = datetime.datetime.now(tz=datetime.timezone.utc)
    date_now_plus_an_hour = date_now + datetime.timedelta(hours=1)
    competition_dict = {
        'name': 'Test',
        'date': date_now_plus_an_hour,
        'open_inscription_during_competition': True,
        'phases': ['test']
    }

    with pytest.raises(CompetitionCreationError):
        Competition.objects.create(**competition_dict)


def test_create_with_a_past_date_fails():
    date_now = datetime.datetime.now(tz=datetime.timezone.utc)
    date_now_minus_an_hour = date_now - datetime.timedelta(hours=1)
    competition_dict = {
        'name': 'Test',
        'date': date_now_minus_an_hour,
        'open_inscription_during_competition': True,
    }

    with pytest.raises(CompetitionPastDateError):
        Competition.objects.create(**competition_dict)
