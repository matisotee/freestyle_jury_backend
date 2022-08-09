from unittest.mock import MagicMock
import pytest

from api_gateway.application.exceptions.competition import CreateCompetitionError
from api_gateway.application.create_competition import CreateCompetitionService
from api_gateway.domain.exceptions.services import CallServiceError
from test.utils import generate_object_id


@pytest.mark.usefixtures('now_date')
def test_create_competition_successfully(now_date):
    """Test create a new competition with valid payload is successful"""
    expected_response = {'name': 'Test Competition', 'status': 'created', 'id': generate_object_id()}
    mock_service_caller = MagicMock()
    mock_service_caller.call.return_value = expected_response
    organizer_id = generate_object_id()
    service = CreateCompetitionService(service_caller=mock_service_caller)

    result = service.create_competition(
        'Test Competition', now_date, organizer_id
    )

    assert result == expected_response
    mock_service_caller.call.assert_called_once_with(
        'competition',
        'create_competition',
        {
            'name': 'Test Competition',
            'date': now_date,
            'organizer_id': organizer_id
        }
    )


@pytest.mark.usefixtures('now_date')
def test_create_competition_with_service_error(now_date):
    mock_service_caller = MagicMock()
    mock_service_caller.call.side_effect = CallServiceError(
        message='Test', code='TEST_CODE'
    )
    service = CreateCompetitionService(service_caller=mock_service_caller)

    with pytest.raises(CreateCompetitionError) as ex_info:
        service.create_competition(
            'Test Competition', now_date, generate_object_id()
        )

    exception = ex_info.value
    assert exception.code == 'TEST_CODE'
