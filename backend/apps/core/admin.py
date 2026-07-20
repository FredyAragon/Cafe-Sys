from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  
from .models import (
    Users, Categories, Products,
    Promotions, ProductsPromotions, Orders, OrderDetails,
    Locations, Reviews, Messages
)

# =====================================================================
# CONTROLES DE USUARIOS Y AUTENTICACIÓN (JWT COMPATIBLE)
# =====================================================================
@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display  = ('id', 'firstName', 'lastName', 'email', 'role', 'status', 'created')
    list_filter   = ('status', 'role')
    search_fields = ('firstName', 'lastName', 'email')
    ordering      = ('lastName', 'firstName')
    
    fields = ('email', 'firstName', 'lastName', 'password', 'role', 'status')

    def save_model(self, request, obj, form, change):
        if obj.status == 'active':
            obj.is_active = True
        else:
            obj.is_active = False

        if obj.role == 'Admin':
            obj.is_staff = True
            obj.is_superuser = True
        elif obj.role in ['Employee', 'Driver']:
            obj.is_staff = True       
            obj.is_superuser = False
        else: # Si es 'Customer'
            obj.is_staff = False
            obj.is_superuser = False

        if not change or form.initial.get('password') != obj.password:
            if not obj.password.startswith('pbkdf2_'):
                obj.set_password(obj.password)
        
        super().save_model(request, obj, form, change)


# =====================================================================
# MAESTROS DEL CATÁLOGO Y PROMOCIONES
# =====================================================================
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'status', 'created')
    list_filter   = ('status',)
    search_fields = ('name',)
    ordering      = ('name',)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'category', 'price', 'status', 'created')
    list_filter   = ('status', 'category')
    search_fields = ('name', 'description')
    ordering      = ('category', 'name')


@admin.register(Promotions)
class PromotionsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'discount', 'discountType', 'startDate', 'endDate', 'status')
    list_filter   = ('status', 'discountType')
    search_fields = ('name', 'description')
    ordering      = ('-startDate',)
    date_hierarchy = 'startDate'
    fields = (
        'name', 'description',
        'discount', 'discountType',
        'imageUrl',
        'startDate', 'endDate',
        'status',
    )
    readonly_fields = ('created', 'modified')


@admin.register(ProductsPromotions)
class ProductsPromotionsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'product', 'promotion', 'status', 'created')
    list_filter   = ('status',)
    search_fields = ('product__name', 'promotion__name')
    ordering      = ('product__name',)


# =====================================================================
# FLUJO DE PEDIDOS Y VENTAS
# =====================================================================
@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'location', 'orderStatus', 'total', 'status', 'created')
    list_filter   = ('orderStatus', 'status')
    search_fields = ('user__firstName', 'user__lastName', 'user__email')
    ordering      = ('-created',)


@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'order', 'product', 'quantity', 'unitPrice', 'subtotal', 'status')
    list_filter   = ('status',)
    search_fields = ('order__id', 'product__name')
    ordering      = ('order',)


@admin.register(Locations)
class LocationsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'alias', 'address', 'isDefault', 'status')
    list_filter   = ('status', 'isDefault')
    search_fields = ('user__firstName', 'user__lastName', 'address', 'alias')
    ordering      = ('user__lastName',)


# =====================================================================
# RESEÑAS Y CANAL DE SOPORTE / ATENCIÓN
# =====================================================================
@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'product', 'rating', 'status', 'created')
    list_filter   = ('status', 'rating')
    search_fields = ('user__email', 'product__name', 'comment')
    ordering      = ('-created',)


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'subject', 'isRead', 'status', 'created')
    list_filter   = ('status', 'isRead')
    search_fields = ('subject', 'body', 'user__email')
    ordering      = ('-created',)