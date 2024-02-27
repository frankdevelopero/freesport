from django.db import models
from django.utils.translation import gettext_lazy as _

class Department(models.Model):
    title = models.CharField(max_length=150, verbose_name=_("Nombre"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creación"))
    status = models.BooleanField(default=True, verbose_name=_("Estado"))

    class Meta:
        verbose_name = "departamento"
        verbose_name_plural = "Departamentos"
        ordering = ['title']

    def __str__(self):
        return self.title


class Province(models.Model):
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL, verbose_name=_("Departamento"))
    title = models.CharField(max_length=150, verbose_name=_("Nombre"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creación"))
    status = models.BooleanField(default=True, verbose_name=_("Estado"))

    class Meta:
        verbose_name = "provincia"
        verbose_name_plural = "Provincias"
        ordering = ['title']

    def __str__(self):
        return self.title


class District(models.Model):
    province = models.ForeignKey(Province, null=True, on_delete=models.SET_NULL, verbose_name=_("Provincia"))
    title = models.CharField(max_length=150, verbose_name=_("Nombre"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creación"))
    status = models.BooleanField(default=True, verbose_name=_("Estado"))

    class Meta:
        verbose_name = "distrito"
        verbose_name_plural = "Distritos"
        ordering = ['title']

    def __str__(self):
        return self.title


