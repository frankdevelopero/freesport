from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from decimal import Decimal
from agent.models import Field, FieldPriceRange
from dashboard.models import Commission
from .models import Booking
from pytz import timezone
from django.utils.dateparse import parse_datetime
import json


@csrf_exempt
@require_http_methods(["POST"])
def booking_api_view(request):
    try:
        data = json.loads(request.body)
        field_id = data.get('fieldId')

        if not field_id:
            return HttpResponseBadRequest("Field ID is required")

        bookings = Booking.objects.filter(
            field_id=field_id,
            status__in=[1, 2]
        ).select_related('user')

        events = []
        for booking in bookings:
            if booking.user:
                title = f"{booking.user.first_name} - {booking.user.phone_number}"
            else:
                title = f"{booking.user_fullname} - {booking.user_phone}"

            event = {
                'title': title,
                'start': booking.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'end': booking.end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'color': 'grey'
            }
            events.append(event)

        return JsonResponse(events, safe=False)
    except Exception as e:
        return HttpResponseBadRequest(f"An error occurred: {str(e)}")


@csrf_exempt
@require_http_methods(["POST"])
def create_booking_view(request):
    try:
        data = json.loads(request.body)
        field_id = data.get('fieldId')
        firstName = data.get('firstName')
        phone = data.get('phone')
        startTime = data.get('startTime')
        endTime = data.get('endTime')

        if not all([field_id, firstName, phone, startTime, endTime]):
            return HttpResponseBadRequest("All fields are required")

        field = Field.objects.filter(id=field_id).select_related('business').first()
        if not field:
            return HttpResponseBadRequest("Invalid field ID")
        start_time = parse_datetime(startTime)
        end_time = parse_datetime(endTime)
        lima_timezone = timezone('America/Lima')
        start_time = lima_timezone.localize(start_time)
        end_time = lima_timezone.localize(end_time)
        booking = Booking(
            user_fullname=firstName,
            user_phone=phone,
            field=field,
            business=field.business,
            start_time=start_time,
            end_time=end_time,
            status=1,
            price=0
        )
        booking.save()
        return JsonResponse({'message': 'Booking created successfully', 'bookingId': booking.id})

    except Exception as e:
        return HttpResponseBadRequest(f"An error occurred: {str(e)}")


@csrf_exempt
@require_http_methods(["POST"])
def data_booking(request):
    try:
        data = json.loads(request.body)
        field_id = data.get('fieldId')
        startTime = data.get('startTime')
        endTime = data.get('endTime')

        if not all([field_id, startTime, endTime]):
            return HttpResponseBadRequest("All fields are required")

        field = Field.objects.filter(id=field_id).select_related('business').first()
        if not field:
            return HttpResponseBadRequest("Invalid field ID")
        start_time = parse_datetime(startTime)
        end_time = parse_datetime(endTime)
        lima_timezone = timezone('America/Lima')
        start_time = lima_timezone.localize(start_time)
        end_time = lima_timezone.localize(end_time)
        print(start_time)
        print(end_time)
        price_ranges = FieldPriceRange.objects.filter(field=field, status=True)
        print(price_ranges)
        total_price = 0
        for price_range in price_ranges:
            if start_time.time() >= price_range.start_time and end_time.time() <= price_range.end_time:
                total_hours = Decimal((end_time - start_time).seconds) / Decimal(3600)
                total_price = price_range.price * total_hours
                break


        commission = Commission.objects.filter(status=True).first()
        print(commission)
        commission_value = 0
        if commission.fee_type == Commission.FLAT:
            commission_value = commission.value
        elif commission.fee_type == Commission.PERCENTAGE:
            commission_value = (commission.value / 100) * total_price

        total_to_pay = total_price + commission_value

        return JsonResponse({
            'priceToPay': total_price,
            'commission': commission_value,
            'totalToPay': total_to_pay
        })

    except Exception as e:
        return HttpResponseBadRequest(f"An error occurred: {str(e)}")
