from django.conf import settings
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.users.views import LoginAPIView, LogoutAPIView, RegistrationAPIView

schema_view = get_schema_view(
    openapi.Info(
        title=settings.OPENAPI_TITLE,
        default_version=settings.OPENAPI_VERSION,
        description=settings.OPENAPI_DESCRIPTION,
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

namespace = 'users'

urlpatterns = [
    path('registration', RegistrationAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('users/', include('api.users.urls'), name='users'),
]

urlpatterns += [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),          # noqa
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),    # noqa
]
