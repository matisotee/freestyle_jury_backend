import pytest


@pytest.mark.usefixtures("authorization_header")
@pytest.mark.usefixtures("now_date")
@pytest.mark.usefixtures("client")
def test_create_competition_successfully(client, now_date, authorization_header):
    """Test create a new competition with valid payload is successful"""
    payload = {
       'name': "Rapublik",
       'date': now_date
    }

    response = client.post('/users/me/competitions/', json=payload, headers=authorization_header)

    assert response.status_code == 200
    assert response.json()['name'] == 'Rapublik'
    assert response.json()['status'] == 'created'
    assert 'id' in response.json()
