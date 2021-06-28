from dataclasses import dataclass


@dataclass
class AuthenticatedUser:
    id: str
    is_superuser: bool


class PermissionService:

    def has_permission(self, authenticated_user: AuthenticatedUser, url: str):
        accessed_object_type = url.split("/")[1]
        accessed_object_id = url.split("/")[2]
        permission_manager = PermissionManagerFactory.get_permission_manager(
            accessed_object_type
        )
        return permission_manager.has_permission(
            authenticated_user, accessed_object_id, accessed_object_type
        )


class PermissionManagerFactory:

    @classmethod
    def get_permission_manager(cls, accessed_object_type: str):

        if accessed_object_type == 'users':
            return UserPermissionManager()

        return DefaultPermissionManager()


class UserPermissionManager:

    def has_permission(
            self,
            authenticated_user: AuthenticatedUser,
            accessed_object_id: str,
            accessed_object_type: str,
    ):

        if not authenticated_user:
            return False

        if accessed_object_id == 'me':
            return True

        if accessed_object_id == authenticated_user.id:
            return True

        if authenticated_user.is_superuser:
            return True

        return False


class DefaultPermissionManager:

    def has_permission(
            self,
            authenticated_user: AuthenticatedUser,
            accessed_object_id: str,
            accessed_object_type: str,
    ):
        return False

