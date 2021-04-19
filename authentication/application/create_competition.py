from dependency_injector.wiring import (
    Provide, inject,
)

from authentication.dependency_injection.containers import Container
from authentication.dependency_injection.decorators import wire

from authentication.domain.service_caller import ServiceCaller


class CreateCompetitionService:

    @wire
    @inject
    def __init__(self, service_caller: ServiceCaller = Provide[Container.service_caller]):
        self.service_caller = service_caller

    def create_competition(self, competition_data):

        body = {
            'name': competition_data['name'],
            'date': competition_data['date'],
            'open_inscription_during_competition': competition_data['open_inscription_during_competition'],
            'organizer': {
                'name': competition_data['authenticated_user']['name'],
                'last_name': competition_data['authenticated_user']['last_name'],
                'aka': competition_data['authenticated_user']['aka'],
                '_id': competition_data['authenticated_user']['_id']
            }
        }
        return self.service_caller.call('competition', 'create_competition', body)
