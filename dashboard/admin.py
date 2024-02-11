from django.contrib import admin
from .models import *

class SportAdmin(admin.ModelAdmin):
    list_display = ('id','title','created_at', 'status')
    search_fields = ['id', 'title', ]



admin.site.register(Sport, SportAdmin)