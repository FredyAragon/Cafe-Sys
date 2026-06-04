from django.contrib import admin
from .models import (
    Roles, Users, Categories, Products, Inventories,
    Promotions, ProductsPromotions, Orders, OrderDetails,
    Locations, Deliveries, Drivers, Vehicles, Reviews, Messages
)


@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'status', 'created')
    list_filter   = ('status',)
    search_fields = ('name',)
    ordering      = ('name',)


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display  = ('id', 'firstName', 'lastName', 'email', 'role', 'status', 'created')
    list_filter   = ('status', 'role')
    search_fields = ('firstName', 'lastName', 'email')
    ordering      = ('lastName', 'firstName')


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


@admin.register(Inventories)
class InventoriesAdmin(admin.ModelAdmin):
    list_display  = ('id', 'product', 'stock', 'minStock', 'status', 'modified')
    list_filter   = ('status',)
    search_fields = ('product__name',)
    ordering      = ('product__name',)


@admin.register(Promotions)
class PromotionsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'discount', 'discountType', 'startDate', 'endDate', 'status')
    list_filter   = ('status', 'discountType')
    search_fields = ('name', 'description')
    ordering      = ('-startDate',)


@admin.register(ProductsPromotions)
class ProductsPromotionsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'product', 'promotion', 'status', 'created')
    list_filter   = ('status',)
    search_fields = ('product__name', 'promotion__name')
    ordering      = ('product__name',)


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


@admin.register(Drivers)
class DriversAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'license', 'phone', 'status', 'created')
    list_filter   = ('status',)
    search_fields = ('license', 'user__firstName', 'user__lastName')
    ordering      = ('license',)


@admin.register(Vehicles)
class VehiclesAdmin(admin.ModelAdmin):
    list_display  = ('id', 'plate', 'model', 'driver', 'status', 'created')
    list_filter   = ('status',)
    search_fields = ('plate', 'model', 'driver__license')
    ordering      = ('plate',)


@admin.register(Deliveries)
class DeliveriesAdmin(admin.ModelAdmin):
    list_display  = ('id', 'order', 'driver', 'vehicle', 'deliveryStatus', 'departureAt', 'deliveredAt', 'status')
    list_filter   = ('deliveryStatus', 'status')
    search_fields = ('order__id', 'driver__license')
    ordering      = ('-created',)


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