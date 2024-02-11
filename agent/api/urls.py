from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessViewSet

router = DefaultRouter()
router.register(r'business', BusinessViewSet)

urlpatterns = [
    path('', include(router.urls)),
]