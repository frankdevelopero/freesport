from django.contrib import admin
from .models import *

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id','title','created_at', 'status')
    search_fields = ['id', 'title', ]



admin.site.register(Department, DepartmentAdmin)
admin.site.register(Province, DepartmentAdmin)
admin.site.register(District, DepartmentAdmin)