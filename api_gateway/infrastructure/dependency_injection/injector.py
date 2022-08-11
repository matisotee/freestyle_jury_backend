def apply_api_gateway_injections():
    from api_gateway.application import (
        authenticate,
        create_competition as create_competition_service,
        register_user as register_user_service,
    )
    from api_gateway.infrastructure.dependency_injection.container import container
    container.wire(modules=[authenticate, create_competition_service, register_user_service])
