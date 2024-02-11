from django.db import models


class Sport(models.Model):
    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Deporte"
        verbose_name_plural = "Deportes"
        ordering = ['title']

    def __str__(self):
        return self.title