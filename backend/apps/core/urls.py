from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView  
from .views import *

router = DefaultRouter()

router.register(r'users', UsersViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'products', ProductsViewSet)
router.register(r'promotions', PromotionsViewSet)
router.register(r'products-promotions', ProductsPromotionsViewSet)
router.register(r'orders', OrdersViewSet)
router.register(r'order-details', OrderDetailsViewSet)
router.register(r'reviews', ReviewsViewSet)
router.register(r'messages', MessagesViewSet)

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('', include(router.urls)),
]