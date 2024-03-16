from django.contrib import admin
from django.urls import path, include
from freesports import settings

admin.site.site_header = 'Freesport Admin'
admin.site.site_title = 'Freesport Adminitrador'
admin.site.index_title = 'Bienvenido, ¿Qué desea gestionar?'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('agente/', include('agent.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', include('frontend.urls')),
    path('', include('users.urls')),
    path('', include('booking.urls')),

    path('api/v1/', include('dashboard.api.urls')),
    path('api/v1/', include('agent.api.urls')),
    path('api/v1/', include('users.api.urls')),

]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
