from dependency_injector import containers, providers

from phase.infra.repositories import MongoCompetitionRepository, MongoPhaseRepository


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    competition_repository = providers.Factory(
        MongoCompetitionRepository
    )

    phase_repository = providers.Factory(
        MongoPhaseRepository
    )


container = Container()
