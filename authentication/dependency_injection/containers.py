from dependency_injector import containers, providers

from authentication.infrastructure.service_callers.frimesh_service_caller import FrimeshServiceCaller


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    service_caller = providers.Factory(
        FrimeshServiceCaller,
    )
