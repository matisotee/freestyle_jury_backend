from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import UserSerializer, VerificationEmailSerializer, VerifyAccountSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class VerificationEmailView(APIView):

    serializer_class = VerificationEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            raise ValidationError('The field provided is not an email', 'EMAIL_INVALID')
        return Response(status=status.HTTP_200_OK)


class VerifyAccountView(APIView):
    serializer_class = VerifyAccountSerializer

    def get(self, request):
        data = {'token': request.GET.get('token')}
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            raise ValidationError('The field provided is not a token', 'TOKEN_INVALID')
        return Response(status=status.HTTP_200_OK)
