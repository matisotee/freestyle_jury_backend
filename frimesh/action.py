from abc import ABC, abstractmethod
from validict import (
    validate,
    FailedValidationError,
)

from frimesh.exceptions import CallActionError


class FrimeshAction(ABC):

    schema = {}

    def validate(self, body):
        try:
            validate(self.schema, body)
        except FailedValidationError:
            raise CallActionError()

    @abstractmethod
    def run(self, **kwargs):
        pass
