from abc import ABC, abstractmethod


class CompetitionRepository(ABC):

    @abstractmethod
    def create(self, competition):
        pass
