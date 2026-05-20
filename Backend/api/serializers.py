from rest_framework import serializers
from .models import *

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class InventoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventories
        fields = '__all__'

class PromotionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotions
        fields = '__all__'

class ProductsPromotionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsPromotions
        fields = '__all__'

class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'

class DriversSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drivers
        fields = '__all__'

class VehiclesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = '__all__'

class DeliveriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliveries
        fields = '__all__'

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'

class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'