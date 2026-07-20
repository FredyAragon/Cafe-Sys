from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.shortcuts import render
from django.conf import settings

from .models import (
    Users, Categories, Products,
    Promotions, ProductsPromotions, Orders, OrderDetails,
    Locations, Reviews, Messages,
    Drivers, Vehicles, Deliveries
)
from .serializers import (
    UsersSerializer, 
    UsersWriteSerializer,
    CategoriesSerializer,
    ProductsSerializer,
    PromotionsSerializer,
    LocationsSerializer,
    ProductsPromotionsSerializer,
    OrdersSerializer, OrderDetailsSerializer,
    ReviewsSerializer,
    MessagesSerializer,
    DriversSerializer,
    VehiclesSerializer,
    DeliveriesSerializer,
)

# apps/core/views.py
from django.shortcuts import render

# URL real de tu despliegue en Vercel
VERCEL_URL = 'https://cafe-sys.vercel.app'  # <-- Aquicito pones el subdominio correcto

def index_gateway_view(request):
    context = {
        'frontend_url': VERCEL_URL,
        'project_description': 'CafeSys es una plataforma integral para la gestión de pedidos y logística de cafeterías.'
    }
    return render(request, 'core/index.html', context)

def home_django_view(request):
    context = {
        'frontend_url': VERCEL_URL,
        'tarjetas': [
            {'front': 'Nuestro Origen', 'back': 'Granos seleccionados de las mejores fincas para garantizar una taza perfecta.'},
            {'front': 'El Ambiente', 'back': 'Un espacio diseñado bajo principios de armonía para que te relajes y disfrutes.'},
            {'front': 'Sabor Único', 'back': 'Tueste artesanal que resalta las notas a chocolate, caramelo y frutos secos.'}
        ]
    }
    return render(request, 'core/home_django.html', context)

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        OrderDetails.objects.filter(product=instance).delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def advance_status(self, request, pk=None):
        order = self.get_object()
        user = request.user

        if not getattr(user, 'is_staff', False) and getattr(user, 'role', '') not in {'Employee', 'Driver'}:
            return Response({'detail': 'No tienes permisos para gestionar órdenes.'}, status=status.HTTP_403_FORBIDDEN)

        next_statuses = {
            'pending': 'assigned',
            'assigned': 'preparing',
            'preparing': 'ready',
            'ready': 'delivered',
        }

        current = order.orderStatus
        next_status = next_statuses.get(current)
        if not next_status:
            return Response({'detail': f'La orden ya está en estado final: {current}'}, status=status.HTTP_400_BAD_REQUEST)

        order.orderStatus = next_status
        order.modified_id = user
        order.save()

        return Response(OrdersSerializer(order, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def archive(self, request, pk=None):
        order = self.get_object()
        user = request.user

        if not getattr(user, 'is_staff', False) and getattr(user, 'role', '') not in {'Employee', 'Driver'}:
            return Response({'detail': 'No tienes permisos para gestionar órdenes.'}, status=status.HTTP_403_FORBIDDEN)

        order.status = 'inactive'
        order.modified_id = user
        order.save()

        return Response(OrdersSerializer(order, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        order = self.get_object()
        user = request.user

        # Solo el dueño de la orden puede cancelarla
        if order.user_id != user.id:
            return Response({'detail': 'Solo puedes cancelar tus propias órdenes.'}, status=status.HTTP_403_FORBIDDEN)

        # Solo se puede cancelar si está en pending
        if order.orderStatus != 'pending':
            return Response({'detail': 'Solo puedes cancelar órdenes en estado pendiente.'}, status=status.HTTP_400_BAD_REQUEST)

        order.orderStatus = 'cancelled'
        order.status = 'inactive'
        order.modified_id = user
        order.save()

        return Response(OrdersSerializer(order, context={'request': request}).data, status=status.HTTP_200_OK)


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

    def get_permissions(self):
        """
        Permitir POST sin autenticación para el formulario de contacto público.
        El resto de operaciones requieren autenticación.
        """
        if self.request.method == 'POST':
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
