from django.urls import path

from authentication.views import CreateUserView

app_name = 'authentication'

urlpatterns = [
    path('user/', CreateUserView.as_view(), name='create_user')
]
