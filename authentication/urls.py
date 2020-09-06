from django.urls import path

from authentication.views import RegisterUserView

app_name = 'authentication'

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
]
