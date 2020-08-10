from django.conf import settings
from django.core.mail import send_mail


class UserMailer:

    EMAIL_VERIFICATION_URL = "/email-verify/"
    EMAIL_VERIFICATION_SUBJECT = 'Verify your email'

    def send_verification_account_email(self, user, token):

        frontend_domain = settings.FRONTEND_DOMAIN
        url = f'http://wwww.{frontend_domain}{self.EMAIL_VERIFICATION_URL}?token={str(token)}'
        body = 'Hola {},\n Utiliza el siguiente link para verificar tu cuenta\n{}'.format(user.name, url)
        send_mail(
            subject=self.EMAIL_VERIFICATION_SUBJECT,
            message=body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email, ]
        )
