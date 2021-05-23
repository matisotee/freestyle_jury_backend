from frimesh.client import FrimeshClient
from frimesh.exceptions import CallActionError

from app.frimesh_services_map import services_map

from api_gateway.application.exceptions.services import CallServiceError
from api_gateway.domain.service_caller import ServiceCaller


class FrimeshServiceCaller(ServiceCaller):

    def call(self, service, action, body):
        client = FrimeshClient(services_map)
        try:
            return client.call(service, action, body)
        except CallActionError as e:
            raise CallServiceError(message=str(e), code=e.code)
