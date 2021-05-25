from django.apps import AppConfig


class ApiGatewayConfig(AppConfig):
    name = 'api_gateway'

    def ready(self):
        from shared.dependency_injection import container
        from shared.dependency_injection.config import INJECTED_MODULES
        container.wire(modules=INJECTED_MODULES)
