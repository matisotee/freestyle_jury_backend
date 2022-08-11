from dependency_injector.wiring import (
    Provide, inject,
)

from api_gateway.application.exceptions.competition import CreateCompetitionError
from api_gateway.domain.exceptions.services import CallServiceError
from api_gateway.domain.service_caller import ServiceCaller
from api_gateway.infrastructure.dependency_injection.container import Container


class CreateCompetitionService:

    @inject
    def __init__(self, service_caller: ServiceCaller = Provide[Container.service_caller]):
        self.service_caller = service_caller

    def create_competition(self, name, date, organizer_id):

        try:
            competition = self.service_caller.call(
                'competition',
                'create_competition',
                {
                    'name': name,
                    'date': date,
                    'organizer_id': organizer_id
                }
            )
            return competition
        except CallServiceError as e:
            raise CreateCompetitionError(message=e.message, code=e.code)
