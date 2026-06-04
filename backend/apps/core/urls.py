from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView  
from .views import *

router = DefaultRouter()

router.register(r'roles', RolesViewSet)
router.register(r'users', UsersViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'products', ProductsViewSet)
router.register(r'inventories', InventoriesViewSet)
router.register(r'promotions', PromotionsViewSet)
router.register(r'products-promotions', ProductsPromotionsViewSet)
router.register(r'locations', LocationsViewSet)
router.register(r'orders', OrdersViewSet)
router.register(r'order-details', OrderDetailsViewSet)
router.register(r'drivers', DriversViewSet)
router.register(r'vehicles', VehiclesViewSet)
router.register(r'deliveries', DeliveriesViewSet)
router.register(r'reviews', ReviewsViewSet)
router.register(r'messages', MessagesViewSet)

# URLs de la aplicación Core
urlpatterns = [
    # Login adaptado para desarrollo local (Usa tu Custom Serializer)
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # NUEVO: Refresco de token para mantener la sesión en Angular
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Endpoints del Router
    path('', include(router.urls)),
]