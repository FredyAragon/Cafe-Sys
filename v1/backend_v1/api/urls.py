from rest_framework import routers
from .views import ProductosViewSet, UsuariosViewSet, PedidosViewSet

router = routers.DefaultRouter()
router.register(r'productos', ProductosViewSet)
router.register(r'usuarios', UsuariosViewSet)
router.register(r'pedidos', PedidosViewSet)

urlpatterns = router.urls