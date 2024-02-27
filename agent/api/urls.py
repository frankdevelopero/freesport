from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessViewSet, AvailableFieldsView, available_fields_view

router = DefaultRouter()
router.register(r'business', BusinessViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search/', AvailableFieldsView.as_view(), name='available-fields'),
    path('search/fields/', available_fields_view, name='search-available-fields'),


]
