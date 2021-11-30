from django.urls import path, include
from authentication.api.views import (
      LoginToken, UserDetail, UserCreateListView
)
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers, permissions

from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Padshare API",
      default_version='v1',
      description="Padshare API documentation",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="dev@padshare.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

app_name = 'authentication'
router = routers.DefaultRouter()
#router.register(r'teams', AccountTeamView)



urlpatterns = [
    path('register', UserCreateListView.as_view(), name='register'),
    #path('teams/', include(router.urls)),
    path('user_detail/<int:pk>/', UserDetail, name='user_detail'),
    path('login', LoginToken.as_view(), name='login'),
    #path('update_pic/<int:pk>/', updatepic_view, name='update_pic'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]
