from rest_framework import viewsets, filters
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


class RolesViewSet(viewsets.ModelViewSet):
    queryset         = Roles.objects.all()
    serializer_class = RolesSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['name']
    ordering_fields  = ['name', 'created']
    ordering         = ['name']


class UsersViewSet(viewsets.ModelViewSet):
    queryset        = Users.objects.select_related('role').all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields   = ['firstName', 'lastName', 'email']
    ordering_fields = ['lastName', 'email', 'created']
    ordering        = ['lastName']

    def get_serializer_class(self):
        # En creación y actualización usar el serializer que acepta passwordHash
        if self.action in ('create', 'update', 'partial_update'):
            return UsersWriteSerializer
        return UsersSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset         = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['name']
    ordering_fields  = ['name', 'created']
    ordering         = ['name']


class ProductsViewSet(viewsets.ModelViewSet):
    # select_related evita N+1 al acceder a product.category en el serializer
    queryset         = Products.objects.select_related('category').all()
    serializer_class = ProductsSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['name', 'description', 'category__name']
    ordering_fields  = ['name', 'price', 'created']
    ordering         = ['category__name', 'name']


class InventoriesViewSet(viewsets.ModelViewSet):
    queryset         = Inventories.objects.select_related('product').all()
    serializer_class = InventoriesSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['product__name']
    ordering_fields  = ['stock', 'product__name']
    ordering         = ['product__name']


class PromotionsViewSet(viewsets.ModelViewSet):
    # Solo mostrar promociones activas por defecto
    queryset         = Promotions.objects.filter(status='active')
    serializer_class = PromotionsSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['name', 'description']
    ordering_fields  = ['name', 'startDate', 'endDate']
    ordering         = ['-startDate']


class ProductsPromotionsViewSet(viewsets.ModelViewSet):
    queryset         = ProductsPromotions.objects.select_related('product', 'promotion').all()
    serializer_class = ProductsPromotionsSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['product__name', 'promotion__name']
    ordering_fields  = ['product__name', 'created']
    ordering         = ['product__name']


class LocationsViewSet(viewsets.ModelViewSet):
    queryset         = Locations.objects.select_related('user').all()
    serializer_class = LocationsSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['address', 'alias', 'user__email']
    ordering_fields  = ['alias', 'created']
    ordering         = ['alias']


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.select_related(
        'user', 'location'
    ).prefetch_related(
        # prefetch_related para la relación inversa details (OneToMany)
        'details', 'details__product'
    ).all()
    serializer_class = OrdersSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['user__firstName', 'user__lastName', 'user__email']
    ordering_fields  = ['created', 'total', 'orderStatus']
    ordering         = ['-created']


class OrderDetailsViewSet(viewsets.ModelViewSet):
    queryset         = OrderDetails.objects.select_related('order', 'product').all()
    serializer_class = OrderDetailsSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['product__name', 'order__id']
    ordering_fields  = ['order', 'product__name', 'created']
    ordering         = ['order']


class DriversViewSet(viewsets.ModelViewSet):
    queryset         = Drivers.objects.select_related('user').all()
    serializer_class = DriversSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['license', 'user__firstName', 'user__lastName']
    ordering_fields  = ['license', 'created']
    ordering         = ['license']


class VehiclesViewSet(viewsets.ModelViewSet):
    queryset         = Vehicles.objects.select_related('driver').all()
    serializer_class = VehiclesSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['plate', 'model', 'driver__license']
    ordering_fields  = ['plate', 'model', 'created']
    ordering         = ['plate']


class DeliveriesViewSet(viewsets.ModelViewSet):
    queryset         = Deliveries.objects.select_related('order', 'driver', 'vehicle').all()
    serializer_class = DeliveriesSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['order__id', 'driver__license']
    ordering_fields  = ['created', 'deliveryStatus', 'departureAt']
    ordering         = ['-created']


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset         = Reviews.objects.select_related('user', 'product').all()
    serializer_class = ReviewsSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['user__email', 'product__name', 'comment']
    ordering_fields  = ['rating', 'created']
    ordering         = ['-created']


class MessagesViewSet(viewsets.ModelViewSet):
    queryset         = Messages.objects.select_related('user').all()
    serializer_class = MessagesSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['subject', 'body', 'user__email']
    ordering_fields  = ['created', 'isRead']
    ordering         = ['-created']