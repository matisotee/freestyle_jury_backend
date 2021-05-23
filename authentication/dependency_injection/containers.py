from dependency_injector import containers, providers

from authentication.infrastructure.authentication.firebase_auth_provider import FirebaseAuthProvider
from authentication.infrastructure.service_callers.frimesh_service_caller import FrimeshServiceCaller


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    service_caller = providers.Factory(
        FrimeshServiceCaller,
    )

    auth_provider = providers.Factory(
        FirebaseAuthProvider,
    )
