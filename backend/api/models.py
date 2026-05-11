# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Carrito(models.Model):
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carrito'


class CarritoDetalle(models.Model):
    pk = models.CompositePrimaryKey('carrito_id', 'producto_id')
    carrito = models.ForeignKey(Carrito, models.DO_NOTHING)
    producto = models.ForeignKey('Productos', models.DO_NOTHING)
    cantidad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'carrito_detalle'


class Categorias(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    imagen_url = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categorias'


class DetallePedidos(models.Model):
    pedido = models.ForeignKey('Pedidos', models.DO_NOTHING)
    producto = models.ForeignKey('Productos', models.DO_NOTHING)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'detalle_pedidos'


class Envios(models.Model):
    pedido = models.OneToOneField('Pedidos', models.DO_NOTHING)
    repartidor = models.ForeignKey('Repartidores', models.DO_NOTHING, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'envios'


class Ingredientes(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    unidad_medida = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ingredientes'


class Inventario(models.Model):
    producto = models.OneToOneField('Productos', models.DO_NOTHING)
    stock = models.IntegerField()
    stock_minimo = models.IntegerField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventario'


class InventarioIngredientes(models.Model):
    ingrediente = models.OneToOneField(Ingredientes, models.DO_NOTHING, blank=True, null=True)
    stock = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventario_ingredientes'


class Mensajes(models.Model):
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING)
    asunto = models.CharField(max_length=150, blank=True, null=True)
    mensaje = models.TextField(blank=True, null=True)
    leido = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mensajes'


class Pedidos(models.Model):
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING)
    ubicacion = models.ForeignKey('Ubicaciones', models.DO_NOTHING)
    estado = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    notas = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pedidos'


class Producciones(models.Model):
    producto = models.ForeignKey('Productos', models.DO_NOTHING, blank=True, null=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, blank=True, null=True)
    cantidad_producida = models.IntegerField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'producciones'


class ProductoIngrediente(models.Model):
    pk = models.CompositePrimaryKey('producto_id', 'ingrediente_id')
    producto = models.ForeignKey('Productos', models.DO_NOTHING)
    ingrediente = models.ForeignKey(Ingredientes, models.DO_NOTHING)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'producto_ingrediente'


class ProductoPromocion(models.Model):
    pk = models.CompositePrimaryKey('producto_id', 'promocion_id')
    producto = models.ForeignKey('Productos', models.DO_NOTHING)
    promocion = models.ForeignKey('Promociones', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'producto_promocion'


class Productos(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen_url = models.CharField(max_length=255, blank=True, null=True)
    categoria = models.ForeignKey(Categorias, models.DO_NOTHING)
    activo = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productos'


class Promociones(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2)
    tipo_descuento = models.CharField(max_length=20)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'promociones'


class Repartidores(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'repartidores'


class Resenas(models.Model):
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING)
    producto = models.ForeignKey(Productos, models.DO_NOTHING)
    calificacion = models.SmallIntegerField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    activo = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'resenas'


class Roles(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class Ubicaciones(models.Model):
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING)
    alias = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=255)
    distrito_id = models.IntegerField(blank=True, null=True)
    referencia = models.TextField(blank=True, null=True)
    predeterminada = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ubicaciones'


class Usuarios(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=150)
    password_hash = models.CharField(max_length=255)
    rol = models.ForeignKey(Roles, models.DO_NOTHING)
    activo = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'
