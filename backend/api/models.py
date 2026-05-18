from django.db import models


class Roles(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.nombre


class Usuarios(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    rol = models.ForeignKey(Roles, on_delete=models.PROTECT)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return self.email


class Categorias(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    imagen_url = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categorias'

    def __str__(self):
        return self.nombre


class Productos(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen_url = models.CharField(max_length=255, blank=True, null=True)
    categoria = models.ForeignKey(Categorias, on_delete=models.PROTECT)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'productos'

    def __str__(self):
        return self.nombre
class ProductoIngrediente(models.Model):
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey('Ingredientes', on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'producto_ingrediente'
        unique_together = ('producto', 'ingrediente')


class ProductoPromocion(models.Model):
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    promocion = models.ForeignKey('Promociones', on_delete=models.CASCADE)

    class Meta:
        db_table = 'producto_promocion'
        unique_together = ('producto', 'promocion')

class Departamentos(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'departamentos'

    def __str__(self):
        return self.nombre
    
class Provincias(models.Model):
    nombre = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamentos, on_delete=models.CASCADE)

    class Meta:
        db_table = 'provincias'

    def __str__(self):
        return self.nombre
    
class Vehiculos(models.Model):
    placa = models.CharField(max_length=20)
    modelo = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'vehiculos'

    def __str__(self):
        return self.placa

class Ubicaciones(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    alias = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=255)
    referencia = models.TextField(blank=True, null=True)
    predeterminada = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ubicaciones'

    def __str__(self):
        return self.direccion

class Ingredientes(models.Model):
    nombre = models.CharField(max_length=100)
    unidad_medida = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ingredientes'


class Promociones(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2)
    tipo_descuento = models.CharField(max_length=20)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'promociones'


class Pedidos(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey('Ubicaciones', on_delete=models.PROTECT)
    estado = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    notas = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pedidos'


class DetallePedidos(models.Model):
    pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_pedidos'