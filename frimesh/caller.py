from abc import ABC, abstractmethod


class NotExistentServiceError(Exception):

    def __init__(self, *args):
        super().__init__(*args)

class ServiceNameError(Exception):

    def __init__(self, *args):
        super().__init__(*args)

class FrimeshCalller(ABC):

    @abstractmethod
    def get_service_map_dict(self):
        """Return a dict { 'service_name': RouterClass } """
        pass

    def call(self, service, action, body):
        if not isinstance(service, str):
            ServiceNameError('Service parameter must be a string')
        service_map = self.get_service_map_dict()
        service_router = service_map.get(service)

        if not service_router:
            NotExistentServiceError(f"The service {service} doesn't exist")

