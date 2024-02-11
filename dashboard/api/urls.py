from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

app_name = "Dashboard"
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
                  path('users/new', UserNewApiView.as_view()),
              ] + router.urls
