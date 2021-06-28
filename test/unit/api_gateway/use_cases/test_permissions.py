from api_gateway.application.permissions import AuthenticatedUser, PermissionService
from test.utils import generate_object_id


def test_has_permission_with_default_permission_manager():
    url = '/default_url/1234/'
    user = AuthenticatedUser(id=generate_object_id(), is_superuser=False)
    service = PermissionService()

    result = service.has_permission(user, url)

    assert result is False


def test_has_permission_with_user_permission_manager():
    user_id  = generate_object_id()
    url = f'/users/{user_id}/'
    user = AuthenticatedUser(id=user_id, is_superuser=False)
    service = PermissionService()

    result = service.has_permission(user, url)

    assert result is True
