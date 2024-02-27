from datetime import datetime

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, viewsets
from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import make_aware
from agent.api.serializers import BusinessSerializer
from agent.models import Business, Field
from booking.models import Booking
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt




def search_available_fields(sport_id, search_date_time, district_id):
    # Convierte la fecha y hora de búsqueda a un objeto datetime y luego a una hora consciente de la zona horaria
    search_datetime = make_aware(datetime.strptime(search_date_time, '%Y-%m-%dT%H:%M:%SZ'))

    # Filtra las empresas por distrito y las canchas por deporte
    available_fields = Field.objects.filter(
        sport_id=sport_id,
        business__district_id=district_id
    ).exclude(
        # Excluye las canchas que tienen una reserva en la fecha y hora de búsqueda
        booking__start_time__lte=search_datetime,
        booking__end_time__gte=search_datetime,
        booking__status__in=[1, 2]  # Considera reservas pendientes y confirmadas
    )

    # Prepara la respuesta con la información de las canchas y las empresas
    response_data = []
    for field in available_fields:
        field_data = {
            "field_id": field.id,
            "field_name": field.name,
            "price_per_hour": field.price_per_hour,
            "requested_datetime": search_date_time,
            "business": {
                "id": field.business.id,
                "title": field.business.title,
                "description": field.business.description,
                "image": field.business.image.url if field.business.image else None,
                "address_display": field.business.address,
                "latitude": field.business.latitude,
                "longitude": field.business.longitude
            }
        }
        response_data.append(field_data)

    return response_data


@csrf_exempt
@require_http_methods(["GET"])  # Asegúrate de que solo se acepten solicitudes GET
def available_fields_view(request):
    sport_id = request.GET.get('sport_id')
    search_date_time = request.GET.get('date_time')
    district_id = request.GET.get('district_id')

    if not all([sport_id, search_date_time, district_id]):
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    available_fields = search_available_fields(sport_id, search_date_time, district_id)
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