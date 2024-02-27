from django.shortcuts import render
from django.views import View

from dashboard.models import Sport
from locations.models import District


# Create your views here.
class IndexView(View):
    def get(self, request):
        districts = District.objects.filter(status=True).select_related('province')
        locations = [(district.title, district.province.title) for district in districts]
        sports = Sport.objects.filter(status=True).values_list('title', flat=True)


        context = {
            'locations': locations,
            'sports': sports
        }
        return render(request, 'frontend/index.html', context)


class SearchView(View):

    def get(self, request):
        districts = District.objects.filter(status=True).select_related('province')
        locations = [(district.title, district.province.title) for district in districts]
        sports = Sport.objects.filter(status=True).values_list('title', flat=True)

        context = {
            'locations': locations,
            'sports': sports
        }
        return render(request, 'frontend/search.html', context)


class DetailView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'frontend/detail.html', context)



class BookingPaymentView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'frontend/booking_payment.html', context)

class BookingConfirmedView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'frontend/booking_confirmed.html', context)
