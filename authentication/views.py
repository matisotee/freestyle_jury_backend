from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from authentication.account_verifier import AccountVerifier
from authentication.serializers import UserSerializer, VerificationEmailSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class VerificationEmailView(generics.CreateAPIView):

    serializer_class = VerificationEmailSerializer
    queryset = get_user_model().objects.all()

    def post(self, request, *args, **kwargs):
        try:
            data = self.serializer_class(request.data).data
            user = get_user_model().objects.get(email=data['email'])
            AccountVerifier.generate_verification_token_for_user(user)
            return Response(status=status.HTTP_200_OK)
        except get_user_model().DoesNotExist:
            raise ValidationError('The email does not belong to a user', 'EMAIL_INVALID')
