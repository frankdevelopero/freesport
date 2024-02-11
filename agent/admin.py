from django.contrib import admin
from .models import *

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('id','title','created_at', 'status')
    search_fields = ['id', 'title', ]

class MediaImageAdmin(admin.ModelAdmin):
    list_display = ('id','image','product', 'created_at')
    search_fields = ['id', 'product', ]

admin.site.register(Business, BusinessAdmin)
admin.site.register(MediaImage, MediaImageAdmin)