from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import RegisterUserSerializer


class RegisterUserView(APIView):
    """Register a new user in the system"""
    serializer_class = RegisterUserSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                raise ValidationError('Missing or invalid fields', 'INVALID_FIELDS')
        except IntegrityError:
            raise ValidationError('This user already exist', 'USER_ALREADY_EXIST')

        return Response(serializer.data, status=status.HTTP_201_CREATED)
