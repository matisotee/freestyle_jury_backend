from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api_gateway.infrastructure.controllers.create_competition import CreateCompetitionView
from api_gateway.infrastructure.controllers.register_user import RegisterUserView

schema_view = get_schema_view(
    openapi.Info(
        title="Freestyle Jury API",
        default_version='v1',
        description="An API for Freestyle Jury application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="matias.sotee@gmail.com"),
        license=openapi.License(name="GNU General Public License v3.0"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

users_patterns = [
    path('competitions/', CreateCompetitionView.as_view(), name='create_competition'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('users/', RegisterUserView.as_view(), name='register_user'),
    url(r'^users/(?P<user_id>\w+|me)/', include(users_patterns)),
]
