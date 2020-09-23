
from rest_framework import serializers
from rest_framework.serializers import Serializer

from authentication.models import User


class RegisterUserSerializer(Serializer):
    """Serializer for the user object"""
    name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)
    aka = serializers.CharField(max_length=25, required=False)
    token = serializers.CharField(max_length=1000, required=True, write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return User.objects.create_user_by_token(
            name=attrs['name'],
            last_name=attrs['last_name'],
            token=attrs['token'],
            aka=attrs.get('aka', '')
        )
