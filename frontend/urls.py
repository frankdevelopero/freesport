from django.urls import path

from frontend.views import *

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('buscar', SearchView.as_view(), name="search"),
    path('detalle/<int:id>/', DetailView.as_view(), name="detail"),
    path('reserva-confirmada/<int:id>/', BookingConfirmedView.as_view(), name="booking_confirmed"),
    path('realizar-pago/<int:id>/', BookingPaymentView.as_view(), name="booking_payment"),
]
