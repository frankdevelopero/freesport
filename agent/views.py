from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
import json

from agent.models import Business


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
        business_id = self.kwargs.get('id')
        business = get_object_or_404(Business, user=request.user)
        fields = business.fields.all()
        fields_data = [{
            'id': field.id,
            'name': field.name,
            'description': field.description,
            'price_per_hour': str(field.price_per_hour),
            'image': request.build_absolute_uri(field.image.url) if field.image else None,
            'sport': field.sport.title,
            'status': field.status
        } for field in fields]

        context = {
            'fields_json': json.dumps(fields_data),
            'business': business
        }
        return render(request, 'agent/agent_booking.html', context)

