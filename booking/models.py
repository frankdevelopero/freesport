from decimal import Decimal
from django.db.models import Q
from django.db import models
from django.utils.translation import gettext_lazy as _

from agent.models import Business, Field
from dashboard.models import Sport
from users.models import User


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Usuario"), null=True, blank=True)
    user_fullname = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("Nombre de la persona"))
    user_phone = models.CharField(max_length=24, null=True, blank=True, verbose_name=_("Número de celular"))
    business = models.ForeignKey(Business, on_delete=models.CASCADE, verbose_name=_("Negocio"))
    voucher = models.ImageField(upload_to='payments', verbose_name=_("Comprobante"), null=True, blank=True)
    phone = models.TextField(max_length=18, null=True, blank=True)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, verbose_name=_("Cancha"))
    start_time = models.DateTimeField(verbose_name=_("Hora de inicio"))
    end_time = models.DateTimeField(verbose_name=_("Hora de fin"))
    status = models.IntegerField(choices=[
        (1, _("Pendiente")),
        (2, _("Confirmada")),
        (3, _("Cancelada")),
        (4, _("Finalizada"))
    ], default=1, verbose_name=_("Estado"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Precio"), editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Reserva")
        verbose_name_plural = _("Reservas")

    def save(self, *args, **kwargs):
        # Encuentra el FieldPriceRange que aplica para el rango de tiempo de la reserva.
        applicable_price_range = self.field.price_ranges.filter(
            Q(start_time__lte=self.start_time.time(), end_time__gte=self.start_time.time()) |
            Q(start_time__lte=self.end_time.time(), end_time__gte=self.end_time.time())
        ).first()

        if applicable_price_range:
            duration_hours = (self.end_time - self.start_time).total_seconds() / 3600
            # Utiliza el precio del rango aplicable para calcular el precio total de la reserva
            self.price = Decimal(duration_hours) * applicable_price_range.price
        else:
            # Maneja el caso en el que no se encuentre un rango de precios aplicable.
            # Podrías establecer un precio por defecto o lanzar un error.
            self.price = Decimal('0.00')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.business.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
