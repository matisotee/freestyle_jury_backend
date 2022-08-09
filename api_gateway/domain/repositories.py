from abc import ABC, abstractmethod


class UserRepository(ABC):

    @abstractmethod
    def create(self, user):
        pass

    @abstractmethod
    def get_by_provider_id(self, provider_id):
        pass
