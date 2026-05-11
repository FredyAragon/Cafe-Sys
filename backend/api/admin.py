from django.contrib import admin
from .models import *

admin.site.register(Roles)
admin.site.register(Usuarios)
admin.site.register(Categorias)
admin.site.register(Productos)
admin.site.register(Ingredientes)
admin.site.register(Promociones)
admin.site.register(Pedidos)
admin.site.register(DetallePedidos)
admin.site.register(Carrito)
admin.site.register(CarritoDetalle)
admin.site.register(ProductoIngrediente)
admin.site.register(ProductoPromocion)