from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.mailer import UserMailer


class AccountVerifier:
    """
    The responsibility of this class is to execute the logic
    to generate a new verification token and verify accounts
    """

    @staticmethod
    def generate_verification_token_for_user(user):
        # TODO: add exception handling and logger
        if user.is_verified:
            raise ValidationError('This user is already verified', 'USER_VERIFIED')
        token = RefreshToken.for_user(user).access_token
        mailer = UserMailer()
        mailer.send_verification_account_email(user, token)
