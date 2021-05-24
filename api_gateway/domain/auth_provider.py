from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ProviderUserData:
    id: str
    email: str
    phone_number: str


class AuthProvider(ABC):

    @abstractmethod
    def get_user_data(self, token: str) -> ProviderUserData:
        pass
