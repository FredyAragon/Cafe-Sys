from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
# 1. IMPORTAMOS LAS VISTAS NATIVAS DE SIMPLE JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Pantalla de bienvenida limpia
def api_welcome_index(request):
    html_content = """
    <html>
        <head>
            <title>CafeSys API Gateway</title>
            <meta charset="utf-8">
        </head>
        <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f6f9; color: #333; margin: 0; padding: 40px; display: flex; justify-content: center; align-items: center; height: 80vh;">
            <div style="background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center; max-width: 500px; width: 100%;">
                <h1 style="color: #2c3e50; margin-top: 10px; font-size: 28px;">CafeSys Backend v1.0</h1>
                <p style="color: #7f8c8d; font-size: 16px; margin-bottom: 30px;">El servidor de producción está operando correctamente en Render conectado a Supabase.</p>
                <div style="display: flex; flex-direction: column; gap: 15px;">
                    <a href="/admin/" style="padding: 12px 20px; background: #417690; color: white; text-decoration: none; border-radius: 6px; font-weight: bold;">
                         Ir al Panel de Control (Django Admin)
                    </a>
                    <a href="/apps/core/" style="padding: 12px 20px; background: #2c3e50; color: white; text-decoration: none; border-radius: 6px; font-weight: bold;">
                         Explorar API Rest (DRF Router)
                    </a>
                </div>
                <p style="margin-top: 30px; font-size: 12px; color: #bdc3c7;">Estructura modular basada en 'Desarrollo de aplicaciones web'</p>
            </div>
        </body>
    </html>
    """
    return HttpResponse(html_content)

# ENRUTADO DEFINITIVO
urlpatterns = [
    # 1. Raíz del sitio (Evita interferir con el router)
    path('', api_welcome_index, name='api-gateway-index'), 
    
    # 2. Panel de administración
    path('admin/', admin.site.urls),
    
    # 3. Módulo de la API 
    path('apps/core/', include('apps.core.urls')), 
    
    # 4. ENDPOINTS ESTRATÉGICOS PARA JWT (Nuevos)
    # Endpoint para hacer LOGIN y obtener los tokens (Access y Refresh)
    path('apps/core/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Endpoint para RENOVAR el access token usando el refresh token sin loguearse de nuevo
    path('apps/core/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]