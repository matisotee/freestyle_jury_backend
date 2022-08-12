from abc import ABC, abstractmethod

from api_gateway.domain.user import User


class UserRepository(ABC):

    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_provider_id(self, provider_id: str) -> User:
        pass

    @abstractmethod
    def delete(self, user_id: str):
        pass
