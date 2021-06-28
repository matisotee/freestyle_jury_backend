from unittest.mock import MagicMock, patch

from api_gateway.application.permissions import PermissionService, AuthenticatedUser

from api_gateway.infrastructure.permissions.django_permissions import DjangoPermissions
from rest_framework.test import APIRequestFactory

from api_gateway.domain.models import User


@patch.object(PermissionService, 'has_permission', return_value=True)
def test_has_permission(mock_has_permission):
    factory = APIRequestFactory()
    user = User(
        _id='5678', provider_id='1234', name='test', last_name='test',
        email='test@test.com', phone_number='1234567', aka='tes'
    )
    view = MagicMock()
    request = factory.get('/default_url/1234/')
    request.user = user
    service = DjangoPermissions()

    result = service.has_permission(request, view)

    assert result is True
    mock_has_permission.assert_called_with(
        AuthenticatedUser(id='5678',  is_superuser=False),
        '/default_url/1234/'
    )
