from dependency_injector import containers, providers

from competition.infrastructure.repositories.competition_repository import MongoCompetitionRepository


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    competition_repository = providers.Factory(
        MongoCompetitionRepository
    )
