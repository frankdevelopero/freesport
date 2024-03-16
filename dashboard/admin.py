from django.contrib import admin
from .models import *


class SportAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'status')
    search_fields = ['id', 'title', ]


class CommissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'fee_type', 'value', 'status', 'created_at')


admin.site.register(Sport, SportAdmin)
admin.site.register(Commission, CommissionAdmin)
