from django.apps import AppConfig


class ApiGatewayConfig(AppConfig):
    name = 'api_gateway'

    def ready(self):
        from api_gateway.application import (
            authenticate,
            create_competition,
            register_user,
        )
        # from api_gateway.infrastructure.django.dependency_injection import Container

        INJECTED_MODULES = [authenticate, create_competition, register_user]
        # container = Container()
        from api_gateway.infrastructure.django.dependency_injection import container
        container.wire(modules=INJECTED_MODULES)
