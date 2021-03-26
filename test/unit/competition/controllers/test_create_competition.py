import collections
import datetime
from unittest.mock import MagicMock, patch

import pytest
import pytz
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from competition.controllers.create_competition import CreateCompetitionView
from competition.exceptions import CompetitionPastDateError
from competition.models.competition import Competition
from competition.services.competition_creator import CompetitionCreator


@pytest.fixture
def now_date():
    return datetime.datetime.now().astimezone(
        pytz.timezone('Etc/GMT+3')
    )


@pytest.fixture
def competition_dict(now_date):
    return {
        'name': "Rapublik",
        'date': now_date.isoformat(),
        'open_inscription_during_competition': True
    }


@pytest.fixture
def organizer_dict():
    return {
        'name': 'Test',
        'last_name': 'Test',
        'aka': 'T',
        '_id': 'test',
    }


@pytest.fixture
def organizer_ordered_dict(organizer_dict):
    organizer_ordered_dict = [
        ('name', organizer_dict['name']),
        ('last_name', organizer_dict['last_name']),
        ('aka', organizer_dict['aka']),
        ('_id', organizer_dict['_id'])
    ]
    return collections.OrderedDict(organizer_ordered_dict)


@patch.object(CompetitionCreator, 'create_competition')
def test_create_competition_successfully(
        mock_create_competition,
        competition_dict,
        organizer_dict,
        organizer_ordered_dict,
        now_date
):

    request = MagicMock()
    request.data = competition_dict.copy()
    request.user.__dict__ = organizer_dict.copy()

    competition_dict['status'] = 'created'
    mock_create_competition.return_value = Competition(**competition_dict)

    result = CreateCompetitionView().post(request)

    assert isinstance(result, Response)
    assert result.data == {
        'name': "Rapublik",
        'status': 'created'
    }
    assert result.status_code == status.HTTP_201_CREATED
    mock_create_competition.assert_called_with(
        organizer_ordered_dict,
        competition_dict['name'],
        now_date,
        competition_dict['open_inscription_during_competition'],
    )


def test_create_competition_without_name_fails(organizer_dict, now_date):

    competition_dict = {
        'date': now_date.isoformat(),
        'open_inscription_during_competition': True
    }

    request = MagicMock()
    request.data = competition_dict
    request.user.__dict__ = organizer_dict

    with pytest.raises(ValidationError):
        CreateCompetitionView().post(request)


def test_create_competition_with_wrong_date_fails(organizer_dict):
    competition_dict = {
        'name': "Rapublik",
        'date': 'test',
        'open_inscription_during_competition': True
    }

    request = MagicMock()
    request.data = competition_dict
    request.user.__dict__ = organizer_dict

    with pytest.raises(ValidationError):
        CreateCompetitionView().post(request)


@patch.object(CompetitionCreator, 'create_competition')
def test_create_competition_with_past_date_fails(
        mock_create_competition, organizer_dict, now_date
):
    mock_create_competition.side_effect = CompetitionPastDateError()

    date = now_date - datetime.timedelta(hours=1)
    date = date.isoformat()

    competition_dict = {
        'name': "Rapublik",
        'date': date,
        'open_inscription_during_competition': True
    }

    request = MagicMock()
    request.data = competition_dict
    request.user.__dict__ = organizer_dict

    with pytest.raises(ValidationError):
        CreateCompetitionView().post(request)
