from django.urls import path

from authentication.views import CreateUserView, VerificationEmailView, VerifyAccountView

app_name = 'authentication'

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='create_user'),
    path('send-verification-email/', VerificationEmailView.as_view(), name='verification_email'),
    path('verify-account/', VerifyAccountView.as_view(), name='verify_account')
]
