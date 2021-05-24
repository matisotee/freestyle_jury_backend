from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from api_gateway.application.exceptions.registration import RegistrationError
from api_gateway.application.register_user import UserRegistrar
from api_gateway.infrastructure.documentation.register_user_view import (
    RESPONSE_201, RESPONSE_400, RESPONSE_401, RESPONSE_403
)
from api_gateway.infrastructure.controllers.base import BaseAPIView, CharField

from utils import feature_flags
from utils.feature_flags.clients import FeatureFlagManager


class RegisterUserRequestSerializer(serializers.Serializer):
    name = CharField(max_length=255, required=True)
    last_name = CharField(max_length=255, required=True)
    aka = CharField(max_length=25, required=False)
    token = CharField(max_length=1000, required=True)


class RegisterUserResponseSerializer(serializers.Serializer):
    id = CharField(max_length=255,)
    name = CharField(max_length=255, required=True)
    last_name = CharField(max_length=255, required=True)
    email = CharField(max_length=255, allow_blank=True, allow_null=True)
    phone_number = CharField(max_length=255, allow_blank=True, allow_null=True)
    aka = CharField(max_length=25, required=False)


class RegisterUserView(BaseAPIView):
    """Register a new user in the system"""
    authentication_classes = []
    permission_classes = []
    request_serializer_class = RegisterUserRequestSerializer
    response_serializer_class = RegisterUserResponseSerializer

    @swagger_auto_schema(
        request_body=RegisterUserRequestSerializer,
        responses={
            201: RESPONSE_201,
            400: RESPONSE_400,
            401: RESPONSE_401,
            403: RESPONSE_403
        }
    )
    def post(self, request, *args, **kwargs):

        if not FeatureFlagManager.is_feature_enabled(
            feature_flags.REGISTER_ENDPOINT
        ):
            raise PermissionDenied(
                'Feature flag disabled for this user',
                code='FEATURE_NOT_AVAILABLE'
            )

        try:
            service = UserRegistrar()
            response = service.register_user(**request.data)
            return Response(response)
        except RegistrationError as e:
            raise ValidationError(e.message, code=e.code)
