from django.urls import path

from agent.views import *

urlpatterns = [
    path('calendario', AgentBookingsView.as_view(), name="agent_bookings"),
]
