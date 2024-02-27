from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User, Code, DocumentType, ResetPasswordRequest

class SettingAdmin(admin.ModelAdmin):
    list_display = ('id','title','created_at', 'status')
    search_fields = ['id', 'title', ]


class UserAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name', 'email', 'created_at', 'status')
    search_fields = ['id', 'first_name', 'email']


class CodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'user', 'used', 'created_at')
    search_fields = ['id', 'number']

class TokenResetPasswordAdmin(admin.ModelAdmin):
    list_display = ('id', 'token', 'status' ,'created_at')
    search_fields = ['id', 'token']


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('email',)


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('id', 'first_name', 'last_name', 'email', 'created_at', 'status', 'get_role_str')
    search_fields = ('id', 'first_name', 'email')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': (
        'email', 'password', 'document_type', 'document_number', 'phone_code', 'phone_number', 'role', 'status')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'document_type', 'document_number',
                       'phone_code', 'phone_number', 'role', 'status'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(form.cleaned_data['password1'])
        super().save_model(request, obj, form, change)

admin.site.register(User, CustomUserAdmin)

admin.site.register(DocumentType, SettingAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(ResetPasswordRequest, TokenResetPasswordAdmin)