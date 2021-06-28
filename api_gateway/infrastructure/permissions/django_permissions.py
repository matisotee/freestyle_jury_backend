from rest_framework.permissions import BasePermission

from api_gateway.application.permissions import AuthenticatedUser, PermissionService


class DjangoPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user:
            user = AuthenticatedUser(
                id=str(request.user._id),
                is_superuser=request.user.is_superuser
            )
        else:
            user = None
        permission_service = PermissionService()
        return permission_service.has_permission(user, request.get_full_path())
