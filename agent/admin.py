from django.contrib import admin
from .models import *

class MediaImageInline(admin.TabularInline):
    model = MediaImage
    extra = 1

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'status')
    search_fields = ['id', 'title', ]

class FieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'business', 'sport', 'price_per_hour')
    search_fields = ['id', 'name', 'business__title']
    inlines = [MediaImageInline, ]


admin.site.register(Business, BusinessAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(MediaImage)
