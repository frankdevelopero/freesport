from django.contrib import admin
from .models import *

class SettingAdmin(admin.ModelAdmin):
    list_display = ('id','title','created_at', 'status')
    search_fields = ['id', 'title', ]


class UserAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name', 'email', 'created_at', 'status')
    search_fields = ['id', 'first_name', 'email']


class CodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'user', 'sid', 'used', 'created_at')
    search_fields = ['id', 'number']

class TokenResetPasswordAdmin(admin.ModelAdmin):
    list_display = ('id', 'token', 'status' ,'created_at')
    search_fields = ['id', 'token']


admin.site.register(DocumentType, SettingAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(ResetPasswordRequest, TokenResetPasswordAdmin)