from dependency_injector.wiring import inject, Provide

from phase.domain.phase import Phase
from phase.domain.repositories import PhaseRepository, CompetitionRepository
from phase.infra.dependency_injection.container import Container


class PhaseCreator:

    @inject
    def __init__(
            self,
            phase_repository: PhaseRepository = Provide[Container.phase_repository],
            competition_repository: CompetitionRepository = Provide[Container.competition_repository]
    ):
        self._phase_repository = phase_repository
        self._competition_repository = competition_repository

    def create_phase(self, competition_id: str, number_of_winners: int, name: str):
        #try:
        competition = self._competition_repository.get_by_id(competition_id)
        previous_phase = None
        query_result = self._phase_repository.get({
            'competition': competition.id,
            'next_phase': None
        })
        if len(query_result) == 1:
            previous_phase = query_result[0]
        phase = Phase.create(number_of_winners, competition, name, previous_phase)
        phase = self._phase_repository.create(phase)

        if previous_phase:
            previous_phase.next_phase = phase.id
            #self._phase_repository
        #except

