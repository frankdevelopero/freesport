from django.db.models import Min, Max
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, viewsets
from django.db.models import Q
from django.utils import timezone
from agent.api.serializers import BusinessSerializer
from agent.models import Business, Field
from booking.models import Booking
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


def search_available_fields(sport_id, search_date_time, district_id, request):
    available_fields = Field.objects.filter(
        sport_id=sport_id,
        business__district_id=district_id
    ).exclude(
        booking__start_time__lte=search_date_time,
        booking__end_time__gte=search_date_time,
        booking__status__in=[1, 2]
    ).prefetch_related('price_ranges', 'business__services')

    response_data = []
    for field in available_fields:
        image_url = field.business.image.url if field.business.image else None
        if image_url:
            image_url = request.build_absolute_uri(image_url)

        # Calcular el precio menor y mayor
        price_range = field.price_ranges.aggregate(
            Min('price'),
            Max('price')
        )
        price_min = price_range['price__min']
        price_max = price_range['price__max']

        # Formatear el rango de precios
        price_range_str = f"S/ {price_min} - {price_max}" if price_min != price_max else f"S/ {price_min}"

        # Recuperar y formatear los servicios del negocio
        services = [{
            "id": service.id,
            "name": service.name,
            "status": service.status
        } for service in field.business.services.all()]

        field_data = {
            "field_id": field.id,
            "field_name": field.name,
            "price_range": price_range_str,
            "requested_datetime": search_date_time,
            "business": {
                "id": field.business.id,
                "title": field.business.title,
                "description": field.business.description,
                "image": image_url,
                "address_display": field.business.address,
                "latitude": field.business.latitude,
                "longitude": field.business.longitude,
                "services": services
            }
        }
        response_data.append(field_data)

    print(response_data)
    return response_data


@csrf_exempt
@require_http_methods(["GET"])
def available_fields_view(request):
    sport_id = request.GET.get('sport_id')
    date_time_str = request.GET.get('date_time')
    date_time = parse_datetime(date_time_str)
    district_id = request.GET.get('district_id')

    if not all([sport_id, date_time, district_id]):
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    available_fields = search_available_fields(sport_id, date_time, district_id, request)
    return JsonResponse(available_fields, safe=False)


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Business.objects.all()


class AvailableFieldsView(generics.ListAPIView):
    serializer_class = BusinessSerializer

    def get_queryset(self):
        sport_id = self.request.query_params.get('sport_id', None)
        district_id = self.request.query_params.get('district_id', None)
        date = self.request.query_params.get('date', None)
        start_time = self.request.query_params.get('start_time', None)
        end_time = self.request.query_params.get('end_time', None)

        queryset = Business.objects.all()

        if district_id:
            queryset = queryset.filter(district_id=district_id)

        if sport_id:
            queryset = queryset.filter(fields__sport_id=sport_id)

        if all([date, start_time, end_time]):
            start_datetime = timezone.make_aware(timezone.datetime.combine(date, start_time))
            end_datetime = timezone.make_aware(timezone.datetime.combine(date, end_time))
            bookings = Booking.objects.filter(
                field__in=Field.objects.filter(business__in=queryset),
                start_time__lt=end_datetime,
                end_time__gt=start_datetime,
            ).values_list('field', flat=True)

            queryset = queryset.filter(
                ~Q(fields__in=bookings) &
                Q(fields__business__in=queryset)
            ).distinct()

        return queryset
