from rest_framework import serializers
from .models import (
    Roles, Users, Categories, Products, Inventories,
    Promotions, ProductsPromotions, Orders, OrderDetails,
    Locations, Deliveries, Drivers, Vehicles, Reviews, Messages
)


# ──────────────────────────────────────────────
# ROLES
# ──────────────────────────────────────────────
class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Roles
        fields = ('id', 'name', 'description', 'status', 'created', 'modified')
        read_only_fields = ('id', 'created', 'modified')


# ──────────────────────────────────────────────
# USERS
# ──────────────────────────────────────────────
class UsersSerializer(serializers.ModelSerializer):
    """Serializer general: nunca expone passwordHash."""
    class Meta:
        model  = Users
        fields = (
            'id', 'firstName', 'lastName', 'email',
            'role', 'status', 'created', 'modified'
        )
        # passwordHash, created_id, modified_id → excluidos totalmente
        read_only_fields = ('id', 'created', 'modified')


class UsersWriteSerializer(serializers.ModelSerializer):
    """Solo para crear/actualizar usuario (incluye passwordHash para escritura)."""
    class Meta:
        model  = Users
        fields = (
            'id', 'firstName', 'lastName', 'email',
            'passwordHash', 'role', 'status'
        )
        read_only_fields = ('id',)
        extra_kwargs = {
            # Nunca devolver el hash en la respuesta
            'passwordHash': {'write_only': True}
        }


# ──────────────────────────────────────────────
# CATEGORIES
# ──────────────────────────────────────────────
class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Categories
        fields = ('id', 'name', 'description', 'imageUrl', 'status', 'created', 'modified')
        read_only_fields = ('id', 'created', 'modified')


# ──────────────────────────────────────────────
# PRODUCTS
# ──────────────────────────────────────────────
class ProductsSerializer(serializers.ModelSerializer):
    # Mostrar nombre de la categoría en lectura (sin reemplazar el FK para escritura)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model  = Products
        fields = (
            'id', 'name', 'description', 'price',
            'imageUrl', 'category', 'category_name',
            'status', 'created', 'modified'
        )
        read_only_fields = ('id', 'category_name', 'created', 'modified')


# ──────────────────────────────────────────────
# INVENTORIES
# ──────────────────────────────────────────────
class InventoriesSerializer(serializers.ModelSerializer):
    # Anidamos el objeto completo del producto con su lógica interna
    product_detail = ProductsSerializer(source='product', read_only=True)

    class Meta:
        model = Inventories
        fields = (
            'id', 'product', 'product_detail',
            'stock', 'minStock', 'status', 'created', 'modified'
        )
        read_only_fields = ('id', 'product_detail', 'created', 'modified')


# ──────────────────────────────────────────────
# PROMOTIONS
# ──────────────────────────────────────────────
class PromotionsSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Promotions
        fields = (
            'id', 'name', 'description', 'discount',
            'discountType', 'startDate', 'endDate',
            'status', 'created', 'modified'
        )
        read_only_fields = ('id', 'created', 'modified')


# ──────────────────────────────────────────────
# PRODUCTS PROMOTIONS
# ──────────────────────────────────────────────
class ProductsPromotionsSerializer(serializers.ModelSerializer):
    product_name   = serializers.CharField(source='product.name',    read_only=True)
    promotion_name = serializers.CharField(source='promotion.name',  read_only=True)

    class Meta:
        model  = ProductsPromotions
        fields = (
            'id', 'product', 'product_name',
            'promotion', 'promotion_name',
            'status', 'created', 'modified'
        )
        read_only_fields = ('id', 'product_name', 'promotion_name', 'created', 'modified')


# ──────────────────────────────────────────────
# LOCATIONS
# ──────────────────────────────────────────────
class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Locations
        fields = (
            'id', 'user', 'alias', 'address',
            'reference', 'isDefault', 'status', 'created', 'modified'
        )
        read_only_fields = ('id', 'created', 'modified')


# ──────────────────────────────────────────────
# ORDERS
# ──────────────────────────────────────────────
class OrderDetailsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderDetails
        fields = (
            'id', 'order', 'product', 'product_name',
            'quantity', 'unitPrice', 'subtotal',
            'status', 'created', 'modified'
        )
        read_only_fields = ('id', 'subtotal', 'product_name', 'created', 'modified')

# Úsalo exclusivamente de forma interna dentro del JSON anidado de órdenes
class ProductDetailNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'name', 'price', 'imageUrl', 'status')

class OrderDetailsNestedSerializer(serializers.ModelSerializer):
    # En lugar de solo el nombre plano, inyectamos el objeto producto completo
    product_detail = ProductDetailNestedSerializer(source='product', read_only=True)

    class Meta:
        model = OrderDetails
        fields = (
            'id', 'product', 'product_detail', 
            'quantity', 'unitPrice', 'subtotal', 'status'
        )
        read_only_fields = ('id', 'subtotal', 'product_detail')

class OrdersSerializer(serializers.ModelSerializer):
    # Cambiamos al serializer anidado avanzado que creamos arriba
    details = OrderDetailsNestedSerializer(many=True, read_only=True)
    # También anidamos los datos básicos del cliente que ordenó
    user_detail = UsersSerializer(source='user', read_only=True)

    class Meta:
        model = Orders
        fields = (
            'id', 'user', 'user_detail', 'location', 'orderStatus',
            'total', 'notes', 'details', 'status', 'created', 'modified'
        )
        read_only_fields = ('id', 'total', 'details', 'user_detail', 'created', 'modified')


# ──────────────────────────────────────────────
# DRIVERS
# ──────────────────────────────────────────────
class DriversSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        if obj.user:
            return f"{obj.user.firstName} {obj.user.lastName}"
        return None

    class Meta:
        model  = Drivers
        fields = (
            'id', 'user', 'user_name',
            'license', 'phone', 'status', 'created', 'modified'
        )
        read_only_fields = ('id', 'user_name', 'created', 'modified')


# ──────────────────────────────────────────────
# VEHICLES
# ──────────────────────────────────────────────
class VehiclesSerializer(serializers.ModelSerializer):
    driver_license = serializers.CharField(source='driver.license', read_only=True)

    class Meta:
        model  = Vehicles
        fields = (
            'id', 'driver', 'driver_license',
            'plate', 'model', 'status', 'created', 'modified'
        )
        read_only_fields = ('id', 'driver_license', 'created', 'modified')


# ──────────────────────────────────────────────
# DELIVERIES
# ──────────────────────────────────────────────
class DeliveriesSerializer(serializers.ModelSerializer):
    # Anidamos la orden básica para saber a dónde va el pedido
    order_detail = OrdersSerializer(source='order', read_only=True)
    # Anidamos al repartidor asignado
    driver_detail = DriversSerializer(source='driver', read_only=True)
    # Anidamos el vehículo asignado
    vehicle_detail = VehiclesSerializer(source='vehicle', read_only=True)

    class Meta:
        model = Deliveries
        fields = (
            'id', 'order', 'order_detail', 
            'driver', 'driver_detail', 
            'vehicle', 'vehicle_detail',
            'deliveryStatus', 'departureAt', 'deliveredAt',
            'status', 'created', 'modified'
        )
        read_only_fields = ('id', 'order_detail', 'driver_detail', 'vehicle_detail', 'deliveredAt', 'created', 'modified')


# ──────────────────────────────────────────────
# REVIEWS
# ──────────────────────────────────────────────
class ReviewsSerializer(serializers.ModelSerializer):
    user_name    = serializers.SerializerMethodField()
    product_name = serializers.CharField(source='product.name', read_only=True)

    def get_user_name(self, obj):
        if obj.user:
            return f"{obj.user.firstName} {obj.user.lastName}"
        return None

    class Meta:
        model  = Reviews
        fields = (
            'id', 'user', 'user_name',
            'product', 'product_name',
            'rating', 'comment',
            'status', 'created', 'modified'
        )
        read_only_fields = ('id', 'user_name', 'product_name', 'created', 'modified')


# ──────────────────────────────────────────────
# MESSAGES
# ──────────────────────────────────────────────
class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Messages
        fields = (
            'id', 'user', 'subject', 'body',
            'isRead', 'status', 'created', 'modified'
        )
        read_only_fields = ('id', 'created', 'modified')