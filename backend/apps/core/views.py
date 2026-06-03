from rest_framework import viewsets, filters, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

from .models import (
    Roles, Users, Categories, Products, Inventories,
    Promotions, ProductsPromotions, Orders, OrderDetails,
    Locations, Deliveries, Drivers, Vehicles, Reviews, Messages
)
from .serializers import (
    RolesSerializer,
    UsersSerializer, UsersWriteSerializer,
    CategoriesSerializer,
    ProductsSerializer,
    InventoriesSerializer,
    PromotionsSerializer,
    ProductsPromotionsSerializer,
    LocationsSerializer,
    OrdersSerializer, OrderDetailsSerializer,
    DriversSerializer,
    VehiclesSerializer,
    DeliveriesSerializer,
    ReviewsSerializer,
    MessagesSerializer,
)


# ──────────────────────────────────────────────
# CUSTOM PERMISSION: Admin writes, anyone reads
# ──────────────────────────────────────────────
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    GET / HEAD / OPTIONS → open to everyone (including anonymous).
    POST / PUT / PATCH / DELETE → only users with is_staff = True.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )


# ──────────────────────────────────────────────
# AUTHENTICATION VIEW
# ──────────────────────────────────────────────
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


# ──────────────────────────────────────────────
# ROLES
# ──────────────────────────────────────────────
class RolesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset         = Roles.objects.all()
    serializer_class = RolesSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['name']
    ordering_fields  = ['name', 'created']
    ordering         = ['name']


# ──────────────────────────────────────────────
# USERS
# ──────────────────────────────────────────────
class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset        = Users.objects.select_related('role').all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields   = ['firstName', 'lastName', 'email']
    ordering_fields = ['lastName', 'email', 'created']
    ordering        = ['lastName']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return UsersWriteSerializer
        return UsersSerializer


# ──────────────────────────────────────────────
# CATEGORIES  →  solo admin puede crear/editar
# ──────────────────────────────────────────────
class CategoriesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]          # ← cambiado
    queryset         = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['name']
    ordering_fields  = ['name', 'created']
    ordering         = ['name']


# ──────────────────────────────────────────────
# PRODUCTS  →  solo admin puede crear/editar
# ──────────────────────────────────────────────
class ProductsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]          # ← cambiado
    queryset         = Products.objects.select_related('category').all()
    serializer_class = ProductsSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['name', 'description', 'category__name']
    ordering_fields  = ['name', 'price', 'created']
    ordering         = ['category__name', 'name']


# ──────────────────────────────────────────────
# INVENTORIES
# ──────────────────────────────────────────────
class InventoriesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset         = Inventories.objects.select_related('product').all()
    serializer_class = InventoriesSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['product__name']
    ordering_fields  = ['stock', 'product__name']
    ordering         = ['product__name']


# ──────────────────────────────────────────────
# PROMOTIONS  →  solo admin puede crear/editar
# ──────────────────────────────────────────────
class PromotionsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]          # ← cambiado
    queryset         = Promotions.objects.filter(status='active')
    serializer_class = PromotionsSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['name', 'description']
    ordering_fields  = ['name', 'startDate', 'endDate']
    ordering         = ['-startDate']


# ──────────────────────────────────────────────
# PRODUCTS PROMOTIONS  →  solo admin
# ──────────────────────────────────────────────
class ProductsPromotionsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]          # ← antes sin permiso
    queryset         = ProductsPromotions.objects.select_related('product', 'promotion').all()
    serializer_class = ProductsPromotionsSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['product__name', 'promotion__name']
    ordering_fields  = ['product__name', 'created']
    ordering         = ['product__name']


# ──────────────────────────────────────────────
# LOCATIONS
# ──────────────────────────────────────────────
class LocationsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset         = Locations.objects.select_related('user').all()
    serializer_class = LocationsSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['address', 'alias', 'user__email']
    ordering_fields  = ['alias', 'created']
    ordering         = ['alias']


# ──────────────────────────────────────────────
# ORDERS
# ──────────────────────────────────────────────
class OrdersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Orders.objects.select_related(
        'user', 'location'
    ).prefetch_related(
        'details', 'details__product'
    ).all()
    serializer_class = OrdersSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['user__firstName', 'user__lastName', 'user__email']
    ordering_fields  = ['created', 'total', 'orderStatus']
    ordering         = ['-created']


# ──────────────────────────────────────────────
# ORDER DETAILS  →  requiere login
# ──────────────────────────────────────────────
class OrderDetailsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]            # ← antes sin permiso
    queryset         = OrderDetails.objects.select_related('order', 'product').all()
    serializer_class = OrderDetailsSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['product__name', 'order__id']
    ordering_fields  = ['order', 'product__name', 'created']
    ordering         = ['order']


# ──────────────────────────────────────────────
# DRIVERS
# ──────────────────────────────────────────────
class DriversViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset         = Drivers.objects.select_related('user').all()
    serializer_class = DriversSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['license', 'user__firstName', 'user__lastName']
    ordering_fields  = ['license', 'created']
    ordering         = ['license']


# ──────────────────────────────────────────────
# VEHICLES
# ──────────────────────────────────────────────
class VehiclesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset         = Vehicles.objects.select_related('driver').all()
    serializer_class = VehiclesSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['plate', 'model', 'driver__license']
    ordering_fields  = ['plate', 'model', 'created']
    ordering         = ['plate']


# ──────────────────────────────────────────────
# DELIVERIES
# ──────────────────────────────────────────────
class DeliveriesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset         = Deliveries.objects.select_related('order', 'driver', 'vehicle').all()
    serializer_class = DeliveriesSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['order__id', 'driver__license']
    ordering_fields  = ['created', 'deliveryStatus', 'departureAt']
    ordering         = ['-created']


# ──────────────────────────────────────────────
# REVIEWS  →  cualquier usuario logueado escribe
# ──────────────────────────────────────────────
class ReviewsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # intencional
    queryset         = Reviews.objects.select_related('user', 'product').all()
    serializer_class = ReviewsSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['user__email', 'product__name', 'comment']
    ordering_fields  = ['rating', 'created']
    ordering         = ['-created']


# ──────────────────────────────────────────────
# MESSAGES
# ──────────────────────────────────────────────
class MessagesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset         = Messages.objects.select_related('user').all()
    serializer_class = MessagesSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['subject', 'body', 'user__email']
    ordering_fields  = ['created', 'isRead']
    ordering         = ['-created']