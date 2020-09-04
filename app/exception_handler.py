from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    try:
        error_data = exc.get_full_details()
    except Exception:
        return response
    response.data = error_data
    return response
