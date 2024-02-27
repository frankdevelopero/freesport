from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from agent.models import Business, Field
from dashboard.models import Sport
from users.models import User


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Usuario"))
    business = models.ForeignKey(Business, on_delete=models.CASCADE, verbose_name=_("Negocio"))
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
        duration_hours = Decimal((self.end_time - self.start_time).total_seconds() / 3600)
        price_per_hour = Decimal(self.field.price_per_hour)
        self.price = price_per_hour * duration_hours
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.business.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
