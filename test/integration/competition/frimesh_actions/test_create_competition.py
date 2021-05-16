import datetime
import pytest
import pytz

from competition.domain.models.competition import Competition
from competition.domain.models.organizer import Organizer
from test.utils import generate_object_id


@pytest.mark.django_db
@pytest.mark.usefixtures("frimesh_client")
def test_create_competition_successfully(frimesh_client):
    """Test create a new competition with valid payload is successful"""
    date_now = datetime.datetime.now(tz=datetime.timezone.utc).astimezone(
        pytz.timezone('America/Argentina/Buenos_Aires')
    )
    date_now_plus_an_hour = date_now + datetime.timedelta(hours=1)
    payload = {
        'name': "Rapublik",
        'date': date_now_plus_an_hour.isoformat(),
        'open_inscription_during_competition': True,
        'organizer': {
            'name': 'Juan',
            'last_name': 'Perez',
            'aka': 'atr',
            '_id': generate_object_id()
        }
    }

    response = frimesh_client.call('competition', 'create_competition', payload)

    assert response == {
        'name': "Rapublik",
        'status': 'created'
    }
    assert Organizer.objects.filter(competitions__name='Rapublik').exists()
    #TODO : Add an assert for the date stored in utc in the DB
    assert Competition.objects.filter(name='Rapublik').exists()
