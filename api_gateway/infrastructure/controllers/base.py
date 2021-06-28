from rest_framework.views import APIView
from rest_framework.views import exception_handler
from rest_framework import serializers


class CharField(serializers.CharField):

    def run_validation(self, data):
        value = super().run_validation(data)
        if not isinstance(data, str):
            self.fail('invalid')
        return value


class ResponseError(Exception):

    def __init__(self, message):
        super().__init__(
            f'Invalid response schema: {message}'
        )


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


class BaseAPIView(APIView):
    request_serializer_class = None
    response_serializer_class = None

    def initial(self, request, *args, **kwargs):

        super().initial(request, *args, **kwargs)

        if not self.request_serializer_class:
            raise RequestSerializerMissingError(self)

        self.request_serializer_class(data=request.data).is_valid(
            raise_exception=True
        )

    def finalize_response(self, request, response, *args, **kwargs):

        if not self.response_serializer_class:
            raise ResponseSerializerMissingError(self)

        if not response.exception:
            try:
                self.response_serializer_class(data=response.data).is_valid(
                    raise_exception=True
                )
            except Exception as e:
                raise ResponseError(str(e))

        return super().finalize_response(request, response, *args, **kwargs)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if not response:
        return None
    if isinstance(response.data, list):
        data = {
            'detail': response.data[0],
            'error_code': response.data[0].code
        }
        response.data = data
        return response
    if isinstance(response.data, dict) and response.data.get('detail'):
        response.data['error_code'] = response.data['detail'].code.upper()
        return response
    if isinstance(response.data, dict):
        data = {
            'detail': 'Missing or invalid fields',
            'error_code': 'FIELDS_ERROR',
            'errors': []
        }
        for key, value in response.data.items():
            field_error = {
                'field': key,
                'detail': value,
            }
            data['errors'].append(field_error)
        response.data = data
        return response
    return response


def decode_user_id(func):
    def inner(self, *args, **kwargs):
        if kwargs.get('user_id', None) == 'me':
            kwargs['user_id'] = str(self.request.user._id)
        return func(self, *args, **kwargs)
    return inner
