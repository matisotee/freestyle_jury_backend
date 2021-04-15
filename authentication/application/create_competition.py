from authentication.domain.service_caller import ServiceCaller


class CreateCompetitionService:

    def __init__(self, service_caller: ServiceCaller):
        self.service_caller = service_caller

    def create_competition(self, body):
        return self.service_caller.call('competition', 'create_competition', body)
