from django.db import models
from django.utils.translation import gettext_lazy as _

from dashboard.models import Sport
from locations.models import Department, Province, District
from users.models import User


class Business(models.Model):
    title = models.CharField(max_length=256, verbose_name=_("Nombre"))
    description = models.TextField(verbose_name=_("Descripción"))
    image = models.ImageField(upload_to='business', verbose_name=_("Imágen principal"))
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name=_("Departamento"))
    province = models.ForeignKey(Province, null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name=_("Provincia"))
    district = models.ForeignKey(District, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("Distrito"))
    latitude = models.FloatField(default=0.0, verbose_name=_("Longitud"))
    longitude = models.FloatField(default=0.0, verbose_name=_("Latitud"))
    address = models.TextField(null=True, blank=True, verbose_name=_("Dirección"))
    reference = models.TextField(null=True, blank=True, verbose_name=_("Referencia"))
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name=_("Usuario admin"))
    promotion = models.BooleanField(default=False, verbose_name=_("Mostrar en inicio"))
    status = models.BooleanField(default=True, verbose_name=_("Estado"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creación"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Fech. actualizado"))

    class Meta:
        verbose_name = "negocio"
        verbose_name_plural = "Negocios"

    def __str__(self):
        return self.title


class Field(models.Model):
    business = models.ForeignKey(Business, related_name='fields', on_delete=models.CASCADE, verbose_name=_("Negocio"))
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name=_("Nombre de la cancha"))
    description = models.TextField(blank=True, verbose_name=_("Descripción"))
    image = models.ImageField(upload_to='fields', verbose_name=_("Imagen"), null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Cancha")
        verbose_name_plural = _("Canchas")

    def __str__(self):
        return f"{self.name} - {self.sport.title} - {self.business.title}"


class BusinessHour(models.Model):
    DAY_CHOICES = [
        (1, _("Lunes")),
        (2, _("Martes")),
        (3, _("Miércoles")),
        (4, _("Jueves")),
        (5, _("Viernes")),
        (6, _("Sábado")),
        (7, _("Domingo")),
    ]

    business = models.ForeignKey(Business, related_name='business_hours', on_delete=models.CASCADE, verbose_name=_("Negocio"))
    day = models.IntegerField(choices=DAY_CHOICES, verbose_name=_("Día de la semana"))
    open_time = models.TimeField(verbose_name=_("Hora de apertura"))
    close_time = models.TimeField(verbose_name=_("Hora de cierre"))

    class Meta:
        verbose_name = _("Horario de negocio")
        verbose_name_plural = _("Horarios de negocios")
        unique_together = ('business', 'day')

    def __str__(self):
        day_name = dict(self.DAY_CHOICES).get(self.day, "-")
        return f"{self.business.title} - {day_name}: {self.open_time.strftime('%H:%M')} - {self.close_time.strftime('%H:%M')}"



class FieldPriceRange(models.Model):
    field = models.ForeignKey(Field, related_name='price_ranges', on_delete=models.CASCADE, verbose_name=_("Cancha"))
    start_time = models.TimeField(verbose_name=_("Hora de inicio"))
    end_time = models.TimeField(verbose_name=_("Hora de fin"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Precio"))
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Precio de cancha")
        verbose_name_plural = _("Precios de canchas")


    def __str__(self):
        return f"{self.field.name} - {self.start_time.strftime('%H:%M')} a {self.end_time.strftime('%H:%M')} - {self.price} PEN"


class Services(models.Model):
    business = models.ForeignKey(Business, related_name='services', on_delete=models.CASCADE, verbose_name=_("Negocio"))
    name = models.CharField(max_length=255, verbose_name=_("Nombre del servicio"))
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Servicio")
        verbose_name_plural = _("Servicios")

    def __str__(self):
        return f"{self.name} - {self.business.title}"


class MediaImage(models.Model):
    image = models.ImageField(upload_to='media_images', verbose_name=_("Imagen"))
    field = models.ForeignKey(Field, on_delete=models.CASCADE, verbose_name=_("Cancha"), null=True, blank=True)
    state = models.BooleanField(default=True, verbose_name=_("Estado"))
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "imagen"
        verbose_name_plural = "imagenes"

    def __str__(self):
        return self.image.url
