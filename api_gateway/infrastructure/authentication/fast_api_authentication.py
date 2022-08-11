from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from api_gateway.application.authenticate import AuthenticationService
from api_gateway.application.exceptions.authentication import AuthenticationError
from api_gateway.infrastructure.controllers.exceptions import HTTPException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def authenticate_with_token(token: str = Depends(oauth2_scheme)):
    try:
        authentication_service = AuthenticationService()
        user = authentication_service.authenticate(token)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=400,
            description=e.message,
            error_code=e.code,
        )
    return user
