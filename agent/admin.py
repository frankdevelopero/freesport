from django.contrib import admin
from .models import *

class MediaImageInline(admin.TabularInline):
    model = MediaImage
    extra = 1

class ServiceInline(admin.TabularInline):
    model =  Services
    extra = 1


class HourInline(admin.TabularInline):
    model =  BusinessHour
    extra = 1

class PriceFieldInline(admin.TabularInline):
    model =  FieldPriceRange
    extra = 1

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'status')
    search_fields = ['id', 'title', ]
    inlines = [ServiceInline, HourInline]

class FieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'business', 'sport')
    search_fields = ['id', 'name', 'business__title']
    inlines = [PriceFieldInline, MediaImageInline]


admin.site.register(Business, BusinessAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(MediaImage)
