from django.contrib import admin
from .models import *

admin.site.register(Roles)
admin.site.register(Usuarios)
admin.site.register(Categorias)
admin.site.register(Productos)
admin.site.register(Ingredientes)
admin.site.register(Promociones)
admin.site.register(Departamentos)
admin.site.register(Provincias)
admin.site.register(Vehiculos)
admin.site.register(Ubicaciones)
admin.site.register(Pedidos)
admin.site.register(DetallePedidos)
admin.site.register(ProductoIngrediente)
admin.site.register(ProductoPromocion)