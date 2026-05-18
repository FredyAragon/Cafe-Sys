from django.db import models


# ================= ROLES =================
class Roles(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.nombre


# ================= USUARIOS =================
class Usuarios(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)

    rol = models.ForeignKey(
        Roles,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return self.email


# ================= CATEGORIAS =================
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


# ================= PRODUCTOS =================
class Productos(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    imagen_url = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    categoria = models.ForeignKey(
        Categorias,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'productos'

    def __str__(self):
        return self.nombre


# ================= INGREDIENTES =================
class Ingredientes(models.Model):
    nombre = models.CharField(max_length=100)
    unidad_medida = models.CharField(max_length=20)

    activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ingredientes'

    def __str__(self):
        return self.nombre


# ================= PRODUCTO_INGREDIENTE =================
class ProductoIngrediente(models.Model):
    producto = models.ForeignKey(
        Productos,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    ingrediente = models.ForeignKey(
        Ingredientes,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'producto_ingrediente'
        unique_together = ('producto', 'ingrediente')


# ================= PROMOCIONES =================
class Promociones(models.Model):
    nombre = models.CharField(max_length=150)

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    descuento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    tipo_descuento = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    fecha_inicio = models.DateField(
        null=True,
        blank=True
    )

    fecha_fin = models.DateField(
        null=True,
        blank=True
    )

    activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'promociones'

    def __str__(self):
        return self.nombre


# ================= PRODUCTO_PROMOCION =================
class ProductoPromocion(models.Model):
    producto = models.ForeignKey(
        Productos,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    promocion = models.ForeignKey(
        Promociones,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'producto_promocion'
        unique_together = ('producto', 'promocion')


# ================= DEPARTAMENTOS =================
class Departamentos(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'departamentos'

    def __str__(self):
        return self.nombre


# ================= PROVINCIAS =================
class Provincias(models.Model):
    nombre = models.CharField(max_length=100)

    departamento = models.ForeignKey(
        Departamentos,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'provincias'

    def __str__(self):
        return self.nombre


# ================= VEHICULOS =================
class Vehiculos(models.Model):
    placa = models.CharField(max_length=20)
    modelo = models.CharField(max_length=100)

    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'vehiculos'

    def __str__(self):
        return self.placa


# ================= UBICACIONES =================
class Ubicaciones(models.Model):
    usuario = models.ForeignKey(
        Usuarios,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    alias = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    direccion = models.CharField(max_length=255)

    referencia = models.TextField(
        blank=True,
        null=True
    )

    predeterminada = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ubicaciones'

    def __str__(self):
        return self.direccion


# ================= PEDIDOS =================
class Pedidos(models.Model):
    usuario = models.ForeignKey(
        Usuarios,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    ubicacion = models.ForeignKey(
        Ubicaciones,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    estado = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    notas = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pedidos'


# ================= DETALLE_PEDIDOS =================
class DetallePedidos(models.Model):
    pedido = models.ForeignKey(
        Pedidos,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    producto = models.ForeignKey(
        Productos,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    cantidad = models.IntegerField(
        null=True,
        blank=True
    )

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'detalle_pedidos'