from unittest.mock import MagicMock
import pytest

from shared.dependency_injection import container

from api_gateway.application.exceptions.competition import CreateCompetitionError
from api_gateway.application.create_competition import CreateCompetitionService
from api_gateway.domain.exceptions.services import CallServiceError


@pytest.mark.usefixtures("now_date")
def test_create_competition_successfully(now_date):
    """Test create a new competition with valid payload is successful"""
    expected_response = {'name': 'Test Competition', 'status': 'created'}
    mock_service_caller = MagicMock()
    mock_service_caller.call.return_value = expected_response
    user = {
        'name': 'test_name',
        'last_name': 'test_last_name',
        'aka': 'test_aka',
        '_id': '1234'
    }

    with container.service_caller.override(mock_service_caller):
        service = CreateCompetitionService()
        result = service.create_competition(
            'Test Competition', now_date, True, user
        )

    assert result == expected_response
    mock_service_caller.call.assert_called()


@pytest.mark.usefixtures("now_date")
def test_create_competition_with_service_error(now_date):
    mock_service_caller = MagicMock()
    mock_service_caller.call.side_effect = CallServiceError(
        message='Test', code='TEST_CODE'
    )
    user = {
        'name': 'test_name',
        'last_name': 'test_last_name',
        'aka': 'test_aka',
        '_id': '1234'
    }
    service = CreateCompetitionService(service_caller=mock_service_caller)

    with pytest.raises(CreateCompetitionError) as ex_info:
        service.create_competition(
            'Test Competition', now_date, True, user
        )

    exception = ex_info.value
    assert exception.code == 'TEST_CODE'
