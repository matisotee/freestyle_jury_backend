from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.mailer import UserMailer


class AccountVerifier:
    """
    The responsibility of this class is to execute the logic
    to generate a new verification token and verify accounts
    """

    @staticmethod
    def start_verification_account_process(email):
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            raise ValidationError('The email does not belong to a user', 'EMAIL_INVALID')
        if user.is_verified:
            raise ValidationError('This user is already verified', 'USER_VERIFIED')
        token = RefreshToken.for_user(user).access_token
        mailer = UserMailer()
        mailer.send_verification_account_email(user, token)
