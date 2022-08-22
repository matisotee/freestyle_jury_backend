from dependency_injector.wiring import inject, Provide

from phase.domain.phase import Competition
from phase.domain.repositories import CompetitionRepository
from phase.infra.dependency_injection.container import Container


class CompetitionUpdater:

    @inject
    def __init__(self, competition_repository: CompetitionRepository = Provide[Container.competition_repository]):
        self._repository = competition_repository

    def update_competition(self, competition_id: str, status: str):
        competition = Competition(id=competition_id, status=status)
        competition = self._repository.create(competition)

        return competition
