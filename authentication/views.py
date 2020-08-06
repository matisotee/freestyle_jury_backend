from django.core.exceptions import ValidationError
from rest_framework import generics, status

from authentication.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer
