from django.shortcuts import render
from django.views import View


# Create your views here.
class IndexView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'frontend/index.html', context)


class SearchView(View):
    def get(self, request):
        context = {

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
