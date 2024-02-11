from django.db import models

from locations.models import Department, Province, District
from users.models import User


class Business(models.Model):
    title = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='business')
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    province = models.ForeignKey(Province, null=True, blank=True, on_delete=models.SET_NULL)
    district = models.ForeignKey(District, null=True, blank=True, on_delete=models.SET_NULL)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    address = models.TextField(null=True, blank=True)
    reference = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Negocio"
        verbose_name_plural = "Negocios"

    def __str__(self):
        return self.title


class MediaImage(models.Model):
    image = models.ImageField(upload_to='business')
    product = models.ForeignKey(Business, on_delete=models.CASCADE)
    state = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imagenes"

    def __str__(self):
        return self.image.url
