from dependency_injector import containers, providers

from api_gateway.infrastructure.authentication.firebase_auth_provider import FirebaseAuthProvider
from api_gateway.infrastructure.repositories.user_repository import MongoUserRepository
from api_gateway.infrastructure.service_callers.frimesh_service_caller import FrimeshServiceCaller


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    service_caller = providers.Factory(
        FrimeshServiceCaller,
    )

    auth_provider = providers.Factory(
        FirebaseAuthProvider,
    )

    user_repository = providers.Factory(
        MongoUserRepository
    )


container = Container()
