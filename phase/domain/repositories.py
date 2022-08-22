from abc import ABC, abstractmethod
from typing import List

from phase.domain.phase import Competition, Phase


class CompetitionRepository(ABC):

    @abstractmethod
    def create(self, competition: Competition) -> Competition:
        pass

    @abstractmethod
    def get_by_id(self, competition_id: str) -> Competition:
        pass


class PhaseRepository(ABC):

    @abstractmethod
    def create(self, phase: Phase) -> Phase:
        pass

    @abstractmethod
    def get(self, query: dict) -> List[Phase]:
        pass
