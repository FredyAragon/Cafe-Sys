# cafesys/urls.py
from django.contrib import admin
from django.urls import path, include
from apps.core.views import index_backend 

urlpatterns = [
    path('', index_backend, name='api-gateway-index'), 
    
    path('admin/', admin.site.urls),
    
    path('apps/core/', include('apps.core.urls')), 
]