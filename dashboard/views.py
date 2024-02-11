from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth import logout, authenticate, login as django_login, update_session_auth_hash, login
from users.forms import LoginForm


class DashboardView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'dashboard/dashboard.html', context)


class AgentView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'dashboard/business/agents.html', context)


class UsersView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'dashboard/users/customer.html', context)


class BookingsView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'dashboard/bookings.html', context)


class AgentNewView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'dashboard/agents_new.html', context)


class UserNewView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'dashboard/users/customers_new.html', context)
