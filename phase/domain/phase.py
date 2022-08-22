from pydantic import BaseModel
from enum import Enum
from typing import Union, List

from phase.domain.exceptions import CompetitionAlreadyStarted, FinalPhaseAlreadyCreated, InvalidNumberOfWinners


class CompetitionStatus(str, Enum):
    created = 'created'
    started = 'started'
    finished = 'finished'


class Competition(BaseModel):
    id: str
    status: CompetitionStatus


class PhaseStatus(str, Enum):
    created = 'created'
    started = 'started'
    finished = 'Finished'


class Phase(BaseModel):
    id: Union[str, None] = None
    team_or_player_quantity: Union[int, None] = None
    number_of_winners: int
    format: Union[str, None] = None
    competition: str
    previous_phase: Union[str, None] = None
    next_phase: Union[str, None] = None
    battles: Union[List[str], None] = None
    status: PhaseStatus
    name: str

    @classmethod
    def create(
            cls,
            number_of_winners: int,
            competition: Competition,
            name: str,
            previous_phase: 'Phase' = None,
    ):
        if competition.status != CompetitionStatus.created:
            raise CompetitionAlreadyStarted()

        if previous_phase and previous_phase.number_of_winners == 1:
            raise FinalPhaseAlreadyCreated()

        team_or_player_quantity = previous_phase.number_of_winners if previous_phase else None

        if team_or_player_quantity and number_of_winners > team_or_player_quantity:
            raise InvalidNumberOfWinners()

        return cls(
            number_of_winners=number_of_winners,
            competition=competition.id,
            name=name,
            status=PhaseStatus.created,
            team_or_player_quantity=team_or_player_quantity,
            previous_phase=previous_phase.id if previous_phase else None
        )
