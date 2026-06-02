from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions
from django.contrib.auth import get_user_model

from .models import (
    Roles, Users, Categories, Products, Inventories,
    Promotions, ProductsPromotions, Orders, OrderDetails,
    Locations, Deliveries, Drivers, Vehicles, Reviews, Messages
)

User = get_user_model()

# ──────────────────────────────────────────────
# ROLES
# ──────────────────────────────────────────────
class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Roles
        fields = ('id', 'name', 'description', 'status', 'created', 'modified')
        read_only_fields = ('id', 'created', 'modified')


# ──────────────────────────────────────────────
# USERS & AUTHENTICATION
# ──────────────────────────────────────────────
class CustomTokenObtainPairSerializer(serializers.Serializer):
    """
    Serializer explícito para el entorno de desarrollo local.
    Acepta tanto 'username' como 'email' sin herencias restrictivas
    y autentica de forma nativa.
    """
    # Declaramos los campos explícitos para la validación inicial de DRF
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # 1. Recuperar la credencial de identidad de forma flexible
        username_input = attrs.get("username") or attrs.get("email")
        password_input = attrs.get("password")

        if not username_input or not password_input:
            raise exceptions.ValidationError({
                "detail": "Se requieren tanto el usuario/email como la contraseña."
            })

        # 2. Localizar al usuario usando el email en minúsculas y limpio
        try:
            user = User.objects.get(email=username_input.lower().strip())
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("No active account found with the given credentials")

        # 3. Validación de contraseña 100% Nativa (Usa el password hasheado por create_superuser)
        if not user.check_password(password_input):
            raise exceptions.AuthenticationFailed("No active account found with the given credentials")

        # 4. Verificar el estado de la cuenta
        if not user.is_active:
            raise exceptions.AuthenticationFailed("Esta cuenta está inactiva.")

        # 5. Emitir los tokens manualmente usando el método de clase nativo
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }


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
        # Ajustado para que coincida con tu campo físico de base de datos
        read_only_fields = ('id',)
        extra_kwargs = {
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


class ProductDetailNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'name', 'price', 'imageUrl', 'status')


class OrderDetailsNestedSerializer(serializers.ModelSerializer):
    product_detail = ProductDetailNestedSerializer(source='product', read_only=True)

    class Meta:
        model = OrderDetails
        fields = (
            'id', 'product', 'product_detail', 
            'quantity', 'unitPrice', 'subtotal', 'status'
        )
        read_only_fields = ('id', 'subtotal', 'product_detail')


class OrdersSerializer(serializers.ModelSerializer):
    details = OrderDetailsNestedSerializer(many=True, read_only=True)
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
    order_detail = OrdersSerializer(source='order', read_only=True)
    driver_detail = DriversSerializer(source='driver', read_only=True)
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