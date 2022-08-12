from abc import ABC, abstractmethod

from competition.domain.competition import Competition


class CompetitionRepository(ABC):

    @abstractmethod
    def create(self, competition: Competition):
        pass
