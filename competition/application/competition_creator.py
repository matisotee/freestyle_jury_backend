from competition.application.exceptions import CompetitionApplicationError
from competition.domain.exceptions import CompetitionPastDateError
from competition.domain.models.competition import Competition
from competition.domain.repositories import CompetitionRepository
from competition.infrastructure.dependency_injection.container import Container

from dependency_injector.wiring import inject, Provide


class CompetitionCreator:

    @inject
    def __init__(self, competition_repository: CompetitionRepository = Provide[Container.competition_repository],):
        self._repository = competition_repository

    def create_competition(self, organizer_id, name, date):

        try:
            competition = Competition.create(name, date, organizer_id)
            competition = self._repository.create(competition)
        except CompetitionPastDateError:
            raise CompetitionApplicationError('Date: set a current or future date', code='PAST_DATE')

        return self._map_competition_to_dict(competition)

    @staticmethod
    def _map_competition_to_dict(competition):
        return {
            'name': competition.name,
            'status': competition.status,
            'id': str(competition._id)
        }
