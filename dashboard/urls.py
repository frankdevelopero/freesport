from django.urls import path

from dashboard.views import *

urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('empresas', AgentView.as_view(), name="dashboard_agents"),
    path('empresas/agregar', AgentNewView.as_view(), name="dashboard_agents_add"),
    path('usuarios', UsersView.as_view(), name="dashboard_users"),
    path('usuarios/agregar', UserNewView.as_view(), name="dashboard_users_add"),
    path('reservas', BookingsView.as_view(), name="dashboard_bookings"),
]
