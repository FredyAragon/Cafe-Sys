from django.db import models


# =========================================================
# ROLES
# =========================================================
class Roles(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.nombre


# =========================================================
# USERS
# =========================================================
class Users(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    password_hash = models.CharField(max_length=255)

    rol = models.ForeignKey(
        Roles,
        on_delete=models.PROTECT
    )

    activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email


# =========================================================
# CATEGORIES
# =========================================================
class Categories(models.Model):
    nombre = models.CharField(max_length=100)

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    imagen_url = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.nombre


# =========================================================
# PRODUCTS
# =========================================================
class Products(models.Model):
    nombre = models.CharField(max_length=150)

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    imagen_url = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    categoria = models.ForeignKey(
        Categories,
        on_delete=models.PROTECT
    )

    activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.nombre


# =========================================================
# INVENTORIES
# =========================================================
class Inventories(models.Model):
    producto = models.OneToOneField(
        Products,
        on_delete=models.CASCADE
    )

    stock = models.IntegerField(default=0)

    stock_minimo = models.IntegerField(default=0)

    unidad_medida = models.CharField(max_length=20)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventories'

    def __str__(self):
        return f"{self.producto.nombre} - {self.stock}"


# =========================================================
# PROMOTIONS
# =========================================================
class Promotions(models.Model):
    nombre = models.CharField(max_length=150)

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    descuento = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    tipo_descuento = models.CharField(max_length=20)

    fecha_inicio = models.DateField()

    fecha_fin = models.DateField()

    activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'promotions'

    def __str__(self):
        return self.nombre


# =========================================================
# PRODUCTS_PROMOTIONS
# =========================================================
class ProductsPromotions(models.Model):
    producto = models.ForeignKey(
        Products,
        on_delete=models.CASCADE
    )

    promocion = models.ForeignKey(
        Promotions,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'products_promotions'
        unique_together = ('producto', 'promocion')


# =========================================================
# LOCATIONS
# =========================================================
class Locations(models.Model):
    usuario = models.ForeignKey(
        Users,
        on_delete=models.CASCADE
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
        db_table = 'locations'

    def __str__(self):
        return self.direccion


# =========================================================
# ORDERS
# =========================================================
class Orders(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('preparando', 'Preparando'),
        ('en_camino', 'En Camino'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(
        Users,
        on_delete=models.CASCADE
    )

    ubicacion = models.ForeignKey(
        Locations,
        on_delete=models.PROTECT
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    notas = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"Pedido #{self.id}"


# =========================================================
# ORDER_DETAILS
# =========================================================
class OrderDetails(models.Model):
    pedido = models.ForeignKey(
        Orders,
        on_delete=models.CASCADE
    )

    producto = models.ForeignKey(
        Products,
        on_delete=models.PROTECT
    )

    cantidad = models.IntegerField()

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        db_table = 'order_details'


# =========================================================
# DRIVERS
# =========================================================
class Drivers(models.Model):
    usuario = models.OneToOneField(
        Users,
        on_delete=models.CASCADE
    )

    licencia = models.CharField(max_length=50)

    telefono = models.CharField(max_length=20)

    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'drivers'

    def __str__(self):
        return self.usuario.nombre


# =========================================================
# VEHICLES
# =========================================================
class Vehicles(models.Model):
    conductor = models.ForeignKey(
        Drivers,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    placa = models.CharField(
        max_length=20,
        unique=True
    )

    modelo = models.CharField(max_length=100)

    color = models.CharField(max_length=50)

    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'vehicles'

    def __str__(self):
        return self.placa


# =========================================================
# DELIVERIES
# =========================================================
class Deliveries(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_camino', 'En Camino'),
        ('entregado', 'Entregado'),
    ]

    pedido = models.OneToOneField(
        Orders,
        on_delete=models.CASCADE
    )

    conductor = models.ForeignKey(
        Drivers,
        on_delete=models.SET_NULL,
        null=True
    )

    vehiculo = models.ForeignKey(
        Vehicles,
        on_delete=models.SET_NULL,
        null=True
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )

    fecha_entrega = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'deliveries'


# =========================================================
# REVIEWS
# =========================================================
class Reviews(models.Model):
    usuario = models.ForeignKey(
        Users,
        on_delete=models.CASCADE
    )

    producto = models.ForeignKey(
        Products,
        on_delete=models.CASCADE
    )

    calificacion = models.IntegerField()

    comentario = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'


# =========================================================
# MESSAGES
# =========================================================
class Messages(models.Model):
    usuario = models.ForeignKey(
        Users,
        on_delete=models.CASCADE
    )

    asunto = models.CharField(max_length=150)

    mensaje = models.TextField()

    leido = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'

    def __str__(self):
        return self.asunto