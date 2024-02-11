from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('agente/', include('agent.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', include('frontend.urls')),
    path('', include('users.urls')),

    path('api/v1/', include('dashboard.api.urls')),
    path('api/v1/', include('agent.api.urls')),
    path('api/v1/', include('users.api.urls')),

]
