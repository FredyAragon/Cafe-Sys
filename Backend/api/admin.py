from django.contrib import admin
from .models import *

admin.site.register(Roles)
admin.site.register(Users)
admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(Inventories)
admin.site.register(Promotions)
admin.site.register(ProductsPromotions)
admin.site.register(Orders)
admin.site.register(OrderDetails)
admin.site.register(Locations)
admin.site.register(Deliveries)
admin.site.register(Drivers)
admin.site.register(Vehicles)
admin.site.register(Reviews)
admin.site.register(Messages)