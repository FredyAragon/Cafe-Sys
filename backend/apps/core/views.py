from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

from .models import (
    Users, Categories, Products,
    Promotions, ProductsPromotions, Orders, OrderDetails,
    Locations, Deliveries, Drivers, Vehicles, Reviews, Messages
)
from .serializers import (
    UsersSerializer, 
    UsersWriteSerializer,
    CategoriesSerializer,
    ProductsSerializer,
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
# AUTHENTICATION VIEW
# ──────────────────────────────────────────────
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Controlador encargado de interceptar el login, omitir las restricciones de email
    y devolver las llaves Access y Refresh validadas bajo la lógica híbrida.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


# ──────────────────────────────────────────────
# USERS
# ──────────────────────────────────────────────
class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset        = Users.objects.all()  
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields   = ['firstName', 'lastName', 'email']
    ordering_fields = ['lastName', 'email', 'created']
    ordering        = ['lastName']

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return UsersWriteSerializer
        return UsersSerializer


# ──────────────────────────────────────────────
# CATEGORIES
# ──────────────────────────────────────────────
class CategoriesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset         = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['name']
    ordering_fields  = ['name', 'created']
    ordering         = ['name']


# ──────────────────────────────────────────────
# PRODUCTS
# ──────────────────────────────────────────────
class ProductsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset         = Products.objects.select_related('category').all()
    serializer_class = ProductsSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['name', 'description', 'category__name']
    ordering_fields  = ['name', 'price', 'created']
    ordering         = ['category__name', 'name']


# ──────────────────────────────────────────────
# PROMOTIONS
# ──────────────────────────────────────────────
class PromotionsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset         = Promotions.objects.filter(status='active')
    serializer_class = PromotionsSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['name', 'description']
    ordering_fields  = ['name', 'startDate', 'endDate']
    ordering         = ['-startDate']


# ──────────────────────────────────────────────
# PRODUCTS PROMOTIONS
# ──────────────────────────────────────────────
class ProductsPromotionsViewSet(viewsets.ModelViewSet):
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

    def get_permissions(self):
        """
        - GET (list/retrieve): AllowAny (público, solo lectura)
        - POST/PUT/PATCH/DELETE: IsAuthenticated
        """
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated()]


# ──────────────────────────────────────────────
# ORDER DETAILS
# ──────────────────────────────────────────────
class OrderDetailsViewSet(viewsets.ModelViewSet):
    queryset         = OrderDetails.objects.select_related('order', 'product').all()
    serializer_class = OrderDetailsSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['product__name', 'order__id']
    ordering_fields  = ['order', 'product__name', 'created']
    ordering         = ['order']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated()]


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
# REVIEWS
# ──────────────────────────────────────────────
class ReviewsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
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