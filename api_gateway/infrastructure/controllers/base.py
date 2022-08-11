from fastapi import Depends
from api_gateway.domain.user import User
from api_gateway.infrastructure.authentication.fast_api_authentication import authenticate_with_token


def get_path_user_id(user_id: str, authenticated_user: User = Depends(authenticate_with_token)):
    if user_id == 'me':
        return str(authenticated_user._id)
    else:
        return user_id
