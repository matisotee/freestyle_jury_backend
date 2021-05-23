from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api_gateway.application.exceptions.services import CallServiceError


class RequestSerializerMissingError(Exception):

    def __init__(self, view):
        super().__init__(
            "Please, add a 'request_serializer_class' attribute in {}".format(type(view).__name__)
        )


class ResponseSerializerMissingError(Exception):

    def __init__(self, view):
        super().__init__(
            "Please, add a 'response_serializer_class' attribute in {}".format(type(view).__name__)
        )


def validate_request_and_response(func):
    def wrapper(*args, **kwargs):
        view = args[0]
        request = args[1]
        try:
            view.request_serializer_class(data=request.data).is_valid(
                raise_exception=True
            )
        except AttributeError:
            raise RequestSerializerMissingError(view)
        try:
            response = func(*args, **kwargs)
        except CallServiceError as e:
            raise ValidationError(e.message, code=e.code)
        try:
            view.response_serializer_class(data=response).is_valid(
                raise_exception=True
            )
        except AttributeError:
            raise ResponseSerializerMissingError(view)

        return Response(response, status=status.HTTP_200_OK)
    return wrapper
