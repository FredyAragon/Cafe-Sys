# cafesys/urls.py
from django.contrib import admin
from django.urls import path, include
from apps.core.views import index_gateway_view, home_django_view

urlpatterns = [
    path('', index_gateway_view, name='index_gateway'), # Tu index actual
    path('home/', home_django_view, name='home_django'), # La nueva Landing Page de Django
    
    path('admin/', admin.site.urls),
    
    path('apps/core/', include('apps.core.urls')), 
]