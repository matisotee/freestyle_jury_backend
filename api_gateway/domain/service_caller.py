from abc import ABC, abstractmethod


class ServiceCaller(ABC):

    @abstractmethod
    def call(self, service: str, action: str, body: dict):
        pass
