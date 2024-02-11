from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View


# Create your views here.
class AgentDashboardView(View):
    @method_decorator(login_required())
    def get(self, request):
        context = {

        }
        return render(request, 'agent/agent_dashboard.html', context)


class AgentBookingsView(View):
    @method_decorator(login_required())
    def get(self, request):
        context = {

        }
        return render(request, 'agent/agent_booking.html', context)
