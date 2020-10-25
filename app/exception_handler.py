from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(response.data, list):
        data = {
            'detail': response.data[0],
            'error_code': response.data[0].code
        }
        response.data = data
        return response
    if isinstance(response.data, dict) and response.data.get('detail'):
        response.data['error_code'] = response.data['detail'].code
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
