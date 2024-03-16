from django.urls import path
from .views import booking_api_view, create_booking_view, data_booking

urlpatterns = [
    path('api/bookings/', booking_api_view, name='booking_api'),
    path('api/create-booking/', create_booking_view, name='create_booking'),
    path('api/data-booking/', data_booking, name='data_booking'),

]
