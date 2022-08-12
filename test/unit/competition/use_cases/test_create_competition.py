import datetime
from unittest.mock import MagicMock

import pytest
import pytz

from competition.application.competition_creator import CompetitionCreator
from competition.application.exceptions import CompetitionApplicationError
from competition.domain.competition import Competition
from test.utils import generate_object_id


@pytest.fixture
def competition():
    date = datetime.datetime.now().astimezone(
        pytz.timezone('Etc/GMT+3')
    ) + datetime.timedelta(hours=1)
    return Competition(
        id=str(generate_object_id()),
        name='Rapublik',
        organizer=generate_object_id(),
        date=date,
        status='created'
    )


def test_create_competition_successfully(competition):
    mock_competition_repository = MagicMock()
    mock_competition_repository.create.return_value = competition
    creator = CompetitionCreator(competition_repository=mock_competition_repository)

    result = creator.create_competition(
        name=competition.name,
        date=competition.date,
        organizer_id=competition.organizer,
    )

    assert competition.name == result.name
    assert competition.status == result.status
    assert str(competition.id) == result.id
    assert mock_competition_repository.create.call_args[0][0].name == competition.name


def test_create_competition_past_date_fails(competition):
    past_date = datetime.datetime.now().astimezone(
        pytz.timezone('Etc/GMT+3')
    ) - datetime.timedelta(hours=1)
    creator = CompetitionCreator()

    with pytest.raises(CompetitionApplicationError) as ex_info:
        creator.create_competition(
            name=competition.name,
            date=past_date,
            organizer_id=competition.organizer
        )
    exception = ex_info.value
    assert exception.code == 'PAST_DATE'
