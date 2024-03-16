from django.db import models
from django.utils.translation import gettext_lazy as _

class Sport(models.Model):
    title = models.CharField(max_length=150, verbose_name=_("Nombre del deporte"))
    image = models.ImageField(upload_to='sports', verbose_name=_("Imagen"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "deporte"
        verbose_name_plural = "Deportes"
        ordering = ['title']

    def __str__(self):
        return self.title

class Commission(models.Model):
    # Definir tipos de tarifa
    FLAT = 'flat'
    PERCENTAGE = 'percentage'
    FEE_TYPES = [
        (FLAT, _('Tarifa plana')),
        (PERCENTAGE, _('Porcentaje')),
    ]

    fee_type = models.CharField(max_length=10, choices=FEE_TYPES, default=PERCENTAGE, verbose_name=_("Tipo de tarifa"))
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Valor"))
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Comisión")
        verbose_name_plural = _("Comisiones")

    def __str__(self):
        return f"Comisión ({self.get_fee_type_display()}): {self.value}"
    def save(self, *args, **kwargs):
        Commission.objects.filter(status=True).update(status=False)
        super().save(*args, **kwargs)