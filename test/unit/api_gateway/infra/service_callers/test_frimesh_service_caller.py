from unittest.mock import patch

import pytest

from api_gateway.domain.exceptions.services import CallServiceError
from api_gateway.infrastructure.service_callers.frimesh_service_caller import FrimeshServiceCaller
from frimesh.client import FrimeshClient
from frimesh.exceptions import CallActionError


@patch.object(FrimeshClient, 'call')
def test_call(mock_frimesh_call):
    service_caller = FrimeshServiceCaller()

    service_caller.call('test_Service', 'test_action', {'key': 'value'})

    mock_frimesh_call.assert_called_once_with(
        'test_Service', 'test_action', {'key': 'value'}
    )


@patch.object(FrimeshClient, 'call')
def test_call_with_service_error(mock_frimesh_call):
    mock_frimesh_call.side_effect = CallActionError('test_message', code='TEST_CODE')
    service_caller = FrimeshServiceCaller()

    with pytest.raises(CallServiceError) as ex_info:
        service_caller.call('test_Service', 'test_action', {'key': 'value'})

    exception = ex_info.value
    assert exception.code == 'TEST_CODE'
