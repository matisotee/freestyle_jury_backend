from abc import ABC, abstractmethod
from validict import (
    validate,
    FailedValidationError,
)

from frimesh.exceptions import ValidationError


class FrimeshAction(ABC):

    schema = {}

    def validate(self, body):
        try:
            validate(self.schema, body)
        except FailedValidationError as e:
            raise ValidationError(str(e))

    @abstractmethod
    def run(self, **kwargs):
        pass
