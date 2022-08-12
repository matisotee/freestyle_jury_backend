from pytz import utc
from competition.domain.exceptions import CompetitionPastDateError
from pydantic import BaseModel
from typing import Union
from enum import Enum
from datetime import datetime


class CompetitionStatus(str, Enum):
    created = 'created'
    started = 'started'
    finished = 'finished'


class Competition(BaseModel):
    id: Union[str, None] = None
    name: str
    date: datetime
    status: CompetitionStatus = CompetitionStatus.created
    organizer: str

    @classmethod
    def create(cls, name: str, date: datetime, organizer_id: str):
        if date < datetime.now(tz=utc):
            raise CompetitionPastDateError('You tried to set a past date to a new competition')
        return cls(name=name, date=date, organizer=organizer_id)
