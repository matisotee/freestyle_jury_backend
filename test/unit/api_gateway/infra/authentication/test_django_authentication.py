from unittest.mock import patch
import pytest
from django.test import RequestFactory
from rest_framework.exceptions import AuthenticationFailed

from api_gateway.application.authenticate import AuthenticationService
from api_gateway.application.exceptions.authentication import AuthenticationError
from api_gateway.domain.models import User
from api_gateway.infrastructure.authentication.django_authentication import DjangoAuthentication


@patch.object(AuthenticationService, 'authenticate')
def test_authenticate(mock_authenticate):
    expected_user = User(
        _id='5678', provider_id='1234', name='test', last_name='test',
        email='test@test.com', phone_number='1234567', aka='tes'
    )
    mock_authenticate.return_value = expected_user
    factory = RequestFactory()
    request = factory.request()
    request.META['HTTP_AUTHORIZATION'] = 'Bearer abcde'
    authenticator = DjangoAuthentication()

    result = authenticator.authenticate(request)

    assert result[0] == expected_user


def test_authenticate_with_no_authorization_header():
    factory = RequestFactory()
    request = factory.request()
    authenticator = DjangoAuthentication()

    with pytest.raises(AuthenticationFailed) as ex_info:
        authenticator.authenticate(request)
    exception = ex_info.value
    assert exception.detail.code == 'NO_TOKEN_PROVIDED'


def test_authenticate_with_no_token():
    factory = RequestFactory()
    request = factory.request()
    request.META['HTTP_AUTHORIZATION'] = 'Bearer '
    authenticator = DjangoAuthentication()

    with pytest.raises(AuthenticationFailed) as ex_info:
        authenticator.authenticate(request)
    exception = ex_info.value
    assert exception.detail.code == 'NO_TOKEN_PROVIDED'


def test_authenticate_with_invalid_token():
    factory = RequestFactory()
    request = factory.request()
    request.META['HTTP_AUTHORIZATION'] = 'Bearer ab dc'
    authenticator = DjangoAuthentication()

    with pytest.raises(AuthenticationFailed) as ex_info:
        authenticator.authenticate(request)
    exception = ex_info.value
    assert exception.detail.code == 'INVALID_TOKEN'


@patch.object(AuthenticationService, 'authenticate')
def test_authenticate_with_authentication_error(mock_authenticate):
    mock_authenticate.side_effect = AuthenticationError('test', 'TEST_CODE')
    factory = RequestFactory()
    request = factory.request()
    request.META['HTTP_AUTHORIZATION'] = 'Bearer abcde'
    authenticator = DjangoAuthentication()

    with pytest.raises(AuthenticationFailed) as ex_info:
        authenticator.authenticate(request)
    exception = ex_info.value
    assert exception.detail.code == 'TEST_CODE'

