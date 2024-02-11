from django.urls import path

from agent.views import *

urlpatterns = [
    path('inicio', AgentDashboardView.as_view(), name="agent_dashboard"),
    path('reservas', AgentBookingsView.as_view(), name="agent_bookings"),

]
