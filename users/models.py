from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

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
    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Tipo de documento"
        verbose_name_plural = "Tipos de documentos"
        ordering = ['title']

    def __str__(self):
        return self.title


class User(AbstractUser):
    objects = CustomUserManager()

    CUSTOMER = 1
    SELLER = 2
    ADMIN = 3
    USER_ROLE = [
        (CUSTOMER, 'Cliente'),
        (SELLER, 'Vendedor'),
        (ADMIN, 'Administrador')
    ]

    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='users/photos', default='users/placeholder.png')
    document_type = models.ForeignKey(DocumentType, null=True, blank=True, on_delete=models.SET_NULL)
    document_number = models.IntegerField(null=True, blank=True)
    phone_code = models.CharField(max_length=8, null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    phone_verified = models.BooleanField(default=False)
    role = models.IntegerField(choices=USER_ROLE, default=ADMIN)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    culqi_id = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'document_number', 'phone_code', 'phone_number']

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

    def has_culqi_id(self) -> bool:
        return True if self.culqi_id else False

    def add_culqi_id(self, culqi_id: str) -> str:
        self.culqi_id = culqi_id
        self.save()

        return self.culqi_id


class ResetPasswordRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Token ResetPassword"
        verbose_name_plural = "Tokens ResetPassword"

    def is_expired(self):
        expiration_time = timezone.now() - timezone.timedelta(hours=24)
        return self.created_at < expiration_time

    def __str__(self):
        return f"ResetPasswordRequest for {self.user.username}"


class Code(models.Model):
    number = models.CharField(max_length=8, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    sid = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = "Código SMS"
        verbose_name_plural = "Códigos SMS"

    def __str__(self):
        return self.number + " " + str(self.user.phone_number) + " " + self.user.email
