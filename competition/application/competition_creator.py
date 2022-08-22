from datetime import datetime

from competition.application.exceptions import CompetitionApplicationError
from competition.domain.exceptions import CompetitionPastDateError
from competition.domain.competition import Competition
from competition.domain.repositories import CompetitionRepository
from competition.infrastructure.dependency_injection.container import Container

from dependency_injector.wiring import inject, Provide
from pubsub import pub


class CompetitionCreator:

    @inject
    def __init__(self, competition_repository: CompetitionRepository = Provide[Container.competition_repository]):
        self._repository = competition_repository

    def create_competition(self, organizer_id: str, name: str, date: datetime) -> Competition:

        try:
            competition = Competition.create(name=name, date=date, organizer_id=organizer_id)
            competition = self._repository.create(competition)
        except CompetitionPastDateError:
            raise CompetitionApplicationError('Date: set a current or future date', code='PAST_DATE')

        pub.sendMessage('competitionUpdated', competition=competition.dict())
        return competition
