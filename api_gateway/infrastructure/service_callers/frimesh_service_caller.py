from frimesh.client import FrimeshClient
from frimesh.exceptions import CallActionError

from shared.frimesh_services_map import services_map

from api_gateway.domain.exceptions.services import CallServiceError
from api_gateway.domain.service_caller import ServiceCaller


class FrimeshServiceCaller(ServiceCaller):

    def call(self, service: str, action: str, body: dict):
        client = FrimeshClient(services_map)
        try:
            return client.call(service, action, body)
        except CallActionError as e:
            raise CallServiceError(message=str(e), code=e.code)
