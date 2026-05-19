from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'roles', RolesViewSet)
router.register(r'users', UsersViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'products', ProductsViewSet)

urlpatterns = router.urls