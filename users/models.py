from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from locations.models import Department, Province, District


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class DocumentType(models.Model):
    title = models.CharField(max_length=150, verbose_name=_("Nombre del documento"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creación"))
    status = models.BooleanField(default=True, verbose_name=_("Estado"))

    class Meta:
        verbose_name = "Tipo de documento"
        verbose_name_plural = "Tipos de documentos"
        ordering = ['title']

    def __str__(self):
        return self.title


class User(AbstractUser):
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    CUSTOMER = 1
    SELLER = 2
    ADMIN = 3
    USER_ROLE = [
        (CUSTOMER, 'Cliente'),
        (SELLER, 'Vendedor'),
        (ADMIN, 'Administrador')
    ]
    username = None
    email = models.EmailField(unique=True, verbose_name=_("Correo electrónico"))
    photo = models.ImageField(upload_to='users/photos', default='users/placeholder.png', null=True, blank=True, verbose_name=_("Foto"))
    document_type = models.ForeignKey(DocumentType, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("Tipo de documento"))
    document_number = models.IntegerField(null=True, blank=True, verbose_name=_("Número de documento"))
    phone_code = models.CharField(max_length=8, null=True, blank=True, verbose_name=_("Codigo pais(+51)"))
    phone_number = models.IntegerField(null=True, blank=True, verbose_name=_("Número de celular"))
    phone_verified = models.BooleanField(default=False, verbose_name=_("Velular verificado"))
    role = models.IntegerField(choices=USER_ROLE, default=ADMIN, verbose_name=_("Tipo de usuario"))
    status = models.BooleanField(default=True, verbose_name=_("Estado"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creación"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Fecha de actualización"))

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_code', 'phone_number']

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def inactive_user(self):
        self.status = False
        self.is_active = False
        self.save()

    def get_role_str(self) -> str:
        return self.get_role_display()


class ResetPasswordRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Usuario"))
    token = models.CharField(max_length=100, unique=True, verbose_name=_("Token"))
    status = models.BooleanField(default=True, verbose_name=_("Estado"))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("Fecha de creación"))

    class Meta:
        verbose_name = "Token ResetPassword"
        verbose_name_plural = "Tokens ResetPassword"

    def is_expired(self):
        expiration_time = timezone.now() - timezone.timedelta(hours=24)
        return self.created_at < expiration_time

    def __str__(self):
        return f"ResetPasswordRequest for {self.user.username}"


class Code(models.Model):
    number = models.CharField(max_length=8, blank=True, verbose_name=_("Código"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Usuario"))
    used = models.BooleanField(default=False, verbose_name=_("Utilizado"))
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_("Fecha de creación"))

    class Meta:
        verbose_name = "Código de verificación"
        verbose_name_plural = "Códigos de verificación"

    def __str__(self):
        return self.number + " " + str(self.user.phone_number) + " " + self.user.email
