from django.contrib.auth import get_user_model

from rest_framework import serializers

from authentication.account_verifier import AccountVerifier


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
    email = serializers.EmailField()

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid()
        if not is_valid:
            return False
        AccountVerifier.start_verification_account_process(self.data['email'])
        return True
