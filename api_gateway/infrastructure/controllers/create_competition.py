from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api_gateway.application.create_competition import CreateCompetitionService
from api_gateway.application.exceptions.competition import CreateCompetitionError
from api_gateway.domain.user import User
from api_gateway.infrastructure.authentication.fast_api_authentication import authenticate_with_token
from api_gateway.infrastructure.controllers.base import get_path_user_id
from api_gateway.infrastructure.controllers.exceptions import HTTPException


router = APIRouter()


class CompetitionDataRequest(BaseModel):
    name: str
    date: datetime


class CompetitionDataResponse(BaseModel):
    name: str
    status: str
    id: str


@router.post("/users/{user_id}/competitions/", response_model=CompetitionDataResponse)
async def create_competition(
        competition_data: CompetitionDataRequest,
        organizer_id: str = Depends(get_path_user_id),
        user: User = Depends(authenticate_with_token)
):
    try:
        service = CreateCompetitionService()
        return service.create_competition(
            name=competition_data.name, date=str(competition_data.date), organizer_id=organizer_id
        )
    except CreateCompetitionError as e:
        raise HTTPException(status_code=400, error_code=e.code, description=e.message)
