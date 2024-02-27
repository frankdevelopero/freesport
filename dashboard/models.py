from django.db import models
from django.utils.translation import gettext_lazy as _

class Sport(models.Model):
    title = models.CharField(max_length=150, verbose_name=_("Nombre del deporte"))
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "deporte"
        verbose_name_plural = "Deportes"
        ordering = ['title']

    def __str__(self):
        return self.title