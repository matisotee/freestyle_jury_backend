import datetime
import pytest
import pytz

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from competition.controllers.create_competition import CreateCompetitionView
from competition.models.competition import Competition
from competition.models.organizer import Organizer

CREATE_COMPETITION_URL = '/competitions/'


@pytest.mark.django_db
@pytest.mark.usefixtures("client")
@pytest.mark.usefixtures("authenticated_user")
def test_create_competition_successfully(authenticated_user, client):
    """Test create a new competition with valid payload is successful"""
    date_now = datetime.datetime.now(tz=datetime.timezone.utc).astimezone(
        pytz.timezone('America/Argentina/Buenos_Aires')
    )
    date_now_plus_an_hour = date_now + datetime.timedelta(hours=1)
    payload = {
        'name': "Rapublik",
        'date': date_now_plus_an_hour.isoformat(),
        'open_inscription_during_competition': True
    }

    factory = APIRequestFactory()
    view = CreateCompetitionView.as_view()
    request = factory.post(CREATE_COMPETITION_URL, payload, format='json')
    force_authenticate(request, user=authenticated_user)
    response = view(request)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {
        'name': "Rapublik",
        'status': 'created'
    }
    assert Organizer.objects.filter(uid=authenticated_user.uid).exists()
    assert Competition.objects.filter(name='Rapublik').exists()

