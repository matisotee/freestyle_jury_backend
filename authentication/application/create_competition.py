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

    def create_competition(self, name, date, open_inscription_during_competition, authenticated_user):

        body = {
            'name': name,
            'date': date,
            'open_inscription_during_competition': open_inscription_during_competition,
            'organizer': {
                'name': authenticated_user['name'],
                'last_name': authenticated_user['last_name'],
                'aka': authenticated_user['aka'],
                '_id': authenticated_user['_id']
            }
        }
        return self.service_caller.call('competition', 'create_competition', body)
