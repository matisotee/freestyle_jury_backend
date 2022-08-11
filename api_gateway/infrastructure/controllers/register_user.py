from typing import Union
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

from api_gateway.application.exceptions.registration import RegistrationError
from api_gateway.application.register_user import UserRegistrar
from api_gateway.infrastructure.controllers.exceptions import HTTPException
from shared.feature_flags import FeatureFlagManager, REGISTER_ENDPOINT


router = APIRouter()


class UserDataRequest(BaseModel):
    name: str
    last_name: str
    aka: Union[str, None] = None
    token: str


class UserDataResponse(BaseModel):
    id: str
    name: str
    last_name: str
    email: EmailStr
    phone_number: Union[str, None] = None
    aka: Union[str, None] = None


@router.post("/users/", response_model=UserDataResponse)
async def register_user(user_data: UserDataRequest):
    if not FeatureFlagManager.is_feature_enabled(
            REGISTER_ENDPOINT
    ):
        raise HTTPException(
            status_code=403, error_code='FEATURE_NOT_AVAILABLE', description='Feature flag disabled for this user'
        )

    try:
        service = UserRegistrar()
        return service.register_user(**user_data.dict())
    except RegistrationError as e:
        raise HTTPException(
            status_code=400, error_code=e.code, description=e.message
        )
