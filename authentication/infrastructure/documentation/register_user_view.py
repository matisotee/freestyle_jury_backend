from drf_yasg import openapi

# POST auth/register/
RESPONSE_201 = openapi.Response(
    description='Created',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
            'aka': openapi.Schema(type=openapi.TYPE_STRING),
        }
    )
)
RESPONSE_400 = openapi.Response(
    description='Bad Request',
    schema=openapi.Schema(
        type=openapi.TYPE_STRING,
        enum=['Missing or invalid fields', 'This user already exist'],
    )
)
RESPONSE_401 = openapi.Response(description='Unauthorized')
RESPONSE_403 = openapi.Response(
    description='Forbidden',
    schema=openapi.Schema(
        type=openapi.TYPE_STRING,
        pattern='{detail: Could not log in.}'
    )
)
