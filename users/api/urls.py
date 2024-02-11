from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, )
from django.urls import path

from .views import *

app_name = "Users"

urlpatterns = [
    path('auth/register', RegisterView.as_view()),
    path('auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/get_token', get_token, name='get_token'),
]