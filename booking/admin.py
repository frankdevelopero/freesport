from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from users.models import User
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'business', 'field', 'start_time', 'end_time', 'status_display', 'price')
    list_filter = ('status', 'business', 'field')
    search_fields = ('user__username', 'business__title', 'field__name')
    readonly_fields = ('price',)

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = _("Estado")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'business', 'field')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Booking, BookingAdmin)
