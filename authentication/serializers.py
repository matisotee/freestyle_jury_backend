from django.contrib.auth import get_user_model

from rest_framework import serializers

from authentication.account_verifier import AccountVerifier
from authentication.authenticator import Authenticator


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""
    password = serializers.CharField(min_length=5, write_only=True)
    aka = serializers.CharField(max_length=25, required=False)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name', 'last_name', 'aka')

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class VerificationEmailSerializer(serializers.Serializer):
    """Serializer for email verification request"""
    email = serializers.EmailField(required=True)

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid()
        if is_valid:
            AccountVerifier.start_verification_account_process(self.data['email'])
        return is_valid


class VerifyAccountSerializer(serializers.Serializer):
    """Serializer for account verification"""
    token = serializers.CharField(required=True)

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid()
        if is_valid:
            AccountVerifier.verify_user_account(self.data['token'])
        return is_valid


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=5, required=True)
    password = serializers.CharField(min_length=5, write_only=True, required=True)
    name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    aka = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return Authenticator.login(
            attrs['email'],
            attrs['password']
        )
