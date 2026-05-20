from rest_framework import viewsets
from .models import *
from .serializers import *

class RolesViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

class InventoriesViewSet(viewsets.ModelViewSet):
    queryset = Inventories.objects.all()
    serializer_class = InventoriesSerializer

class PromotionsViewSet(viewsets.ModelViewSet):
    queryset = Promotions.objects.all()
    serializer_class = PromotionsSerializer

class ProductsPromotionsViewSet(viewsets.ModelViewSet):
    queryset = ProductsPromotions.objects.all()
    serializer_class = ProductsPromotionsSerializer

class LocationsViewSet(viewsets.ModelViewSet):
    queryset = Locations.objects.all()
    serializer_class = LocationsSerializer

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

class OrderDetailsViewSet(viewsets.ModelViewSet):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer

class DriversViewSet(viewsets.ModelViewSet):
    queryset = Drivers.objects.all()
    serializer_class = DriversSerializer

class VehiclesViewSet(viewsets.ModelViewSet):
    queryset = Vehicles.objects.all()
    serializer_class = VehiclesSerializer

class DeliveriesViewSet(viewsets.ModelViewSet):
    queryset = Deliveries.objects.all()
    serializer_class = DeliveriesSerializer

class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer

class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer