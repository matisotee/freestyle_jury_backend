from abc import ABC, abstractmethod


class AuthProvider(ABC):

    @abstractmethod
    def get_user_id(self, token: str) -> str:
        pass
