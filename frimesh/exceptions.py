class InvalidServiceMapError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NotExistentServiceError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NotExistentActionError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ServiceNameError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ActionNameError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BodyError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ActionError(Exception):

    def __init__(self, message, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(message)


class CallActionError(Exception):

    def __init__(self, message, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(message)


class ServerError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ValidationError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)