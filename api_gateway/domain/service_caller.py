from abc import ABC, abstractmethod


class ServiceCaller(ABC):

    @abstractmethod
    def call(self, service, action, body):
        pass
