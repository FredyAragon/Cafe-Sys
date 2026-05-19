from django.contrib import admin
from .models import *

admin.site.register(Productos)
admin.site.register(Usuarios)
admin.site.register(Pedidos)
admin.site.register(Categorias)
admin.site.register(Promociones)
admin.site.register(Ingredientes)
admin.site.register(ProductoIngrediente)
admin.site.register(ProductoPromocion)
admin.site.register(Roles)
admin.site.register(Ubicaciones)
admin.site.register(DetallePedidos)