from fastapi import Depends

from api_gateway.domain.exceptions.user import NotExistentUserError
from api_gateway.domain.repositories import UserRepository
from api_gateway.domain.user import User
from api_gateway.infrastructure.authentication.fast_api_authentication import authenticate_with_token
from api_gateway.infrastructure.controllers.exceptions import HTTPException
from api_gateway.infrastructure.repositories.user_repository import MongoUserRepository


def get_path_user_id(
        user_id: str,
        authenticated_user: User = Depends(authenticate_with_token),
        user_repository: UserRepository = Depends(MongoUserRepository)
) -> str:
    if user_id == 'me':
        return str(authenticated_user.id)

    try:
        user_repository.get_by_id(user_id)
    except NotExistentUserError:
        raise HTTPException(
            status_code=400, error_code='NON_EXISTENT_USER', description='The user id in the url is invalid'
        )
    return user_id
