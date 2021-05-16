from frimesh.exceptions import (
    ActionError,
    ActionNameError,
    BodyError,
    CallActionError,
    InvalidServiceMapError,
    NotExistentActionError,
    NotExistentServiceError,
    ServerError,
    ServiceNameError, ValidationError,
)


class FrimeshClient:

    def __init__(self, service_map):
        if not isinstance(service_map, dict):
            raise InvalidServiceMapError('The server map must ve a dictionary')
        self.service_map = service_map

    def call(self, service, action, body):
        if not isinstance(service, str):
            raise ServiceNameError('Service parameter must be a string')
        if not isinstance(action, str):
            raise ActionNameError('Action parameter must be a string')
        if not isinstance(body, dict):
            raise BodyError('The body param must be a dictionary')

        services_map = self.service_map
        actions_map = services_map.get(service)

        if not actions_map:
            NotExistentServiceError(f"The service {service} is not registered in the map")

        action_class = actions_map.get(action)

        if not action_class:
            NotExistentActionError(f"The action {action} doesn't exist")

        action_obj = action_class()
        try:
            deserialized_body = action_obj.validate(body)
            return action_obj.run(**deserialized_body)
        except ActionError as e:
            raise CallActionError(str(e), **e.__dict__)
        except ValidationError as e:
            raise ServerError(
                f'Error validating the call to "{service}" service in action "{action}". '
                f'ValidationError: {str(e)}'
            )
        except Exception as e:
            raise ServerError(
                f'Error during the call to "{service}" service in action "{action}". '
                f'{str(type(e))}: {str(e)}'
            )
