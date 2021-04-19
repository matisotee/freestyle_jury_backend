from django.db import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from api_documentation.register_user_view import (
    RESPONSE_201, RESPONSE_400, RESPONSE_401, RESPONSE_403
)
from authentication.serializers import RegisterUserSerializer
from utils import feature_flags
from utils.feature_flags.clients import FeatureFlagManager


class RegisterUserView(APIView):
    """Register a new user in the system"""
    serializer_class = RegisterUserSerializer
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        request_body=RegisterUserSerializer,
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
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
        except IntegrityError:
            raise ValidationError('This user already exist', 'USER_ALREADY_EXIST')

        return Response(serializer.data, status=status.HTTP_201_CREATED)
