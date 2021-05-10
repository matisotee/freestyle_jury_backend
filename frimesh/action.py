from abc import ABC, abstractmethod
from marshmallow import ValidationError as MarshmallowValidationError

from frimesh.exceptions import ValidationError


class FrimeshAction(ABC):

    schema = {}

    def validate(self, body):
        try:
            result = self.schema().load(body)
        except MarshmallowValidationError as err:
            raise ValidationError(str(err.messages))

        return result

    @abstractmethod
    def run(self, **kwargs):
        pass
