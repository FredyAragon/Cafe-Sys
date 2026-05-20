from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'roles', RolesViewSet)
router.register(r'users', UsersViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'products', ProductsViewSet)
router.register(r'inventories',         InventoriesViewSet)
router.register(r'promotions',          PromotionsViewSet)
router.register(r'products-promotions', ProductsPromotionsViewSet)
router.register(r'locations',           LocationsViewSet)
router.register(r'orders',              OrdersViewSet)
router.register(r'order-details',       OrderDetailsViewSet)
router.register(r'drivers',             DriversViewSet)
router.register(r'vehicles',            VehiclesViewSet)
router.register(r'deliveries',          DeliveriesViewSet)
router.register(r'reviews',             ReviewsViewSet)
router.register(r'messages',            MessagesViewSet)

urlpatterns = router.urls