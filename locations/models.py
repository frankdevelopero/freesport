from django.db import models


class Department(models.Model):
    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ['title']

    def __str__(self):
        return self.title


class Province(models.Model):
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
        ordering = ['title']

    def __str__(self):
        return self.title


class District(models.Model):
    province = models.ForeignKey(Province, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"
        ordering = ['title']

    def __str__(self):
        return self.title


