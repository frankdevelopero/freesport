from django.shortcuts import redirect
from django.db.models import Min, Max
from django.views import View
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from agent.models import Business, Field, BusinessHour
from booking.models import Booking
from dashboard.models import Sport
from locations.models import District
from django.utils.http import urlencode
from django.utils.dateparse import parse_datetime
import json


# Create your views here.
class IndexView(View):
    def get(self, request):
        districts = District.objects.filter(status=True).select_related('province').values('id', 'title',
                                                                                           'province__title')
        locations = [{'id': district['id'], 'name': f"{district['title']}, {district['province__title']}"} for district
                     in districts]
        sports_json = [{'id': sport.id, 'name': sport.title} for sport in Sport.objects.filter(status=True)]
        sports = Sport.objects.filter(status=True)
        business = Business.objects.filter(promotion=True)  ##Agregar price: rango de precio menor y mayor de fields
        context = {
            'locations': locations,
            'sports': sports_json,
            'sports_items': sports,
            'business': business
        }
        return render(request, 'frontend/index.html', context)


class SearchView(View):

    def get(self, request):
        districts = District.objects.filter(status=True).select_related('province').values('id', 'title',
                                                                                           'province__title')
        locations = [{'id': district['id'], 'name': f"{district['title']}, {district['province__title']}"} for district
                     in districts]
        sports = [{'id': sport.id, 'name': sport.title} for sport in Sport.objects.filter(status=True)]
        print(sports)
        print(locations)
        context = {
            'locations_json': json.dumps(locations, cls=DjangoJSONEncoder),
            'sports_json': json.dumps(sports, cls=DjangoJSONEncoder)
        }
        return render(request, 'frontend/search.html', context)

    def post(self, request):
        sport_id = request.POST.get('sport')
        district_id = request.POST.get('city')
        date = request.POST.get('date')
        time = request.POST.get('time')
        print(f"Sport ID: {sport_id}, District ID: {district_id}, Date: {date}, Time: {time}")
        try:
            search_date = datetime.strptime(date, '%Y-%m-%d')
            search_time = datetime.strptime(time, '%H:%M').time()
            search_datetime = timezone.make_aware(datetime.combine(search_date, search_time))
        except ValueError as e:
            print(f"Error al convertir fecha/hora: {e}")

        print(sport_id)
        print(district_id)
        queryset = self.search_fields(sport_id, district_id, search_datetime)

        context = {
            'search_results': queryset,
            'locations': [(district.id, district.title, district.province.title) for district in
                          District.objects.filter(status=True).select_related('province')],
            'sports': Sport.objects.filter(status=True).values_list('id', 'title')
        }

        print(str(context))
        return render(request, 'frontend/search.html', context)

    def search_fields(self, sport_id, district_id, search_datetime):
        queryset = Business.objects.prefetch_related('fields').filter(
            fields__sport_id=sport_id,
            district_id=district_id,
            fields__status=True,
        )

        start_datetime = search_datetime
        end_datetime = search_datetime + timedelta(hours=1)

        booked_fields = Booking.objects.filter(
            field__in=Field.objects.filter(business__in=queryset),
            start_time__lt=end_datetime,
            end_time__gt=start_datetime,
            status__in=[1, 2]
        ).values_list('field', flat=True)

        queryset = queryset.exclude(fields__in=booked_fields).distinct()

        return queryset


class DetailView(View):
    def get(self, request, *args, **kwargs):
        business_id = self.kwargs.get('id')
        business = get_object_or_404(Business, id=business_id)
        services = business.services.all()
        fields = business.fields.all().prefetch_related('price_ranges')

        business_hours = BusinessHour.objects.filter(business=business_id)
        business_hours_json = [
            {
                'daysOfWeek': [bh.day],
                'startTime': bh.open_time.strftime("%H:%M"),
                'endTime': bh.close_time.strftime("%H:%M"),
            } for bh in business_hours
        ]

        business_price_min = None
        business_price_max = None

        fields_data = []
        for field in fields:
            price_range = field.price_ranges.aggregate(Min('price'), Max('price'))
            price_min = price_range['price__min']
            price_max = price_range['price__max']
            if business_price_min is None or (price_min is not None and price_min < business_price_min):
                business_price_min = price_min
            if business_price_max is None or (price_max is not None and price_max > business_price_max):
                business_price_max = price_max

            price_range_str = f"S/ {price_min} - {price_max}" if price_min != price_max else f"S/ {price_min}"

            field_data = {
                'id': field.id,
                'name': field.name,
                'description': field.description,
                'price_range': price_range_str,
                'image': field.image.url if field.image else None,
                'sport': field.sport.title,
                'status': field.status
            }
            fields_data.append(field_data)

        # Formatear el rango de precios del negocio
        business_price_range_str = f"S/ {business_price_min} - {business_price_max}" if business_price_min != business_price_max else f"S/ {business_price_min}"

        images = []
        for field in fields:
            images.extend(field.mediaimage_set.filter(state=True))

        context = {
            'business': business,
            'business_price_range': business_price_range_str,
            'fields': fields,
            'images': images,
            'fields_json': json.dumps(fields_data, ensure_ascii=False),
            'services': services,
            'business_hours_json': business_hours_json,
        }
        return render(request, 'frontend/detail.html', context)


class BookingPaymentView(View):
    def get(self, request, *args, **kwargs):
        field_id = self.kwargs.get('id')
        field = get_object_or_404(Field, id=field_id)

        context = {
            'field': field,
            'user_authenticated': request.user.is_authenticated
        }
        return render(request, 'frontend/booking_payment.html', context)

    def post(self, request, *args, **kwargs):
        field_id = request.POST.get('field_id')
        field = get_object_or_404(Field, id=field_id)
        phone = request.POST.get('phone')
        voucher = request.FILES.get('voucher')
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        start_time = parse_datetime(start_time_str)
        end_time = parse_datetime(end_time_str)

        booking = Booking(
            user=request.user,
            business=field.business,
            phone=phone,
            voucher=voucher,
            field=field,
            start_time=start_time,
            end_time=end_time,
            status=1,
            price=0
        )
        booking.save()

        return redirect('booking_confirmed', id=booking.id)


class BookingConfirmedView(View):
    def get(self, request, *args, **kwargs):
        booking_id = self.kwargs.get('id')
        booking = get_object_or_404(Booking, id=booking_id)

        context = {
            'booking': booking
        }
        return render(request, 'frontend/booking_confirmed.html', context)
