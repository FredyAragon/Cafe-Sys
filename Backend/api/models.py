from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.core.exceptions import ValidationError
from django.utils import timezone


# =========================================================
# VALIDATORS
# =========================================================
def validate_not_blank(value):
    if not value or not value.strip():
        raise ValidationError('This field cannot be blank or whitespace.')

def validate_http_url(value):
    if value and not value.startswith('http'):
        raise ValidationError('URL must start with http or https.')

def validate_end_date(instance):
    if instance.endDate and instance.startDate:
        if instance.endDate < instance.startDate:
            raise ValidationError('End date must be greater than or equal to start date.')

def validate_delivery_dates(instance):
    if instance.deliveredAt and instance.departureAt:
        if instance.deliveredAt < instance.departureAt:
            raise ValidationError('Delivered date cannot be before departure date.')


# =========================================================
# ROLES
# =========================================================
class Roles(models.Model):
    name        = models.CharField(
                    max_length=50,
                    unique=True,
                    validators=[validate_not_blank]
                  )
    description = models.TextField(blank=True, null=True)
    status      = models.CharField(
                    max_length=20,
                    default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')]
                  )
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    created_id  = models.ForeignKey(
                    'Users',
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='roles_created'
                  )
    modified_id = models.ForeignKey(
                    'Users',
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='roles_modified'
                  )

    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name


# =========================================================
# USERS
# =========================================================
class Users(models.Model):
    firstName    = models.CharField(
                     max_length=100,
                     validators=[validate_not_blank]
                   )
    lastName     = models.CharField(
                     max_length=100,
                     validators=[validate_not_blank]
                   )
    email        = models.EmailField(unique=True)
    passwordHash = models.CharField(
                     max_length=255,
                     validators=[MinLengthValidator(8)]
                   )
    role         = models.ForeignKey(
                     Roles,
                     on_delete=models.PROTECT,
                     related_name='users'
                   )
    status       = models.CharField(
                     max_length=20,
                     default='active',
                     choices=[('active', 'Active'), ('inactive', 'Inactive')]
                   )
    created      = models.DateTimeField(auto_now_add=True)
    modified     = models.DateTimeField(auto_now=True)
    created_id   = models.ForeignKey(
                     'self',
                     on_delete=models.SET_NULL,
                     null=True, blank=True,
                     related_name='users_created'
                   )
    modified_id  = models.ForeignKey(
                     'self',
                     on_delete=models.SET_NULL,
                     null=True, blank=True,
                     related_name='users_modified'
                   )

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


# =========================================================
# CATEGORIES
# =========================================================
class Categories(models.Model):
    name        = models.CharField(
                    max_length=100,
                    unique=True,
                    validators=[validate_not_blank]
                  )
    description = models.TextField(blank=True, null=True)
    imageUrl    = models.CharField(
                    max_length=255,
                    blank=True, null=True,
                    validators=[validate_http_url]
                  )
    status      = models.CharField(
                    max_length=20,
                    default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')]
                  )
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    created_id  = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='categories_created'
                  )
    modified_id = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='categories_modified'
                  )

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


# =========================================================
# PRODUCTS
# =========================================================
class Products(models.Model):
    name        = models.CharField(
                    max_length=150,
                    validators=[validate_not_blank]
                  )
    description = models.TextField(blank=True, null=True)
    price       = models.DecimalField(
                    max_digits=10,
                    decimal_places=2,
                    validators=[MinValueValidator(0.01)]
                  )
    imageUrl    = models.CharField(
                    max_length=255,
                    blank=True, null=True,
                    validators=[validate_http_url]
                  )
    category    = models.ForeignKey(
                    Categories,
                    on_delete=models.PROTECT,
                    related_name='products'
                  )
    status      = models.CharField(
                    max_length=20,
                    default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')]
                  )
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    created_id  = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='products_created'
                  )
    modified_id = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='products_modified'
                  )

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


# =========================================================
# INVENTORIES
# =========================================================
class Inventories(models.Model):
    product     = models.OneToOneField(
                    Products,
                    on_delete=models.CASCADE,
                    related_name='inventory'
                  )
    stock       = models.IntegerField(
                    default=0,
                    validators=[MinValueValidator(0)]
                  )
    minStock    = models.IntegerField(
                    default=5,
                    validators=[MinValueValidator(0)]
                  )
    status      = models.CharField(
                    max_length=20,
                    default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')]
                  )
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    created_id  = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='inventories_created'
                  )
    modified_id = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='inventories_modified'
                  )

    class Meta:
        db_table = 'inventories'
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'

    def __str__(self):
        return f"{self.product.name} - stock: {self.stock}"


# =========================================================
# PROMOTIONS
# =========================================================
class Promotions(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed',      'Fixed Amount'),
    ]

    name         = models.CharField(
                     max_length=150,
                     validators=[validate_not_blank]
                   )
    description  = models.TextField(blank=True, null=True)
    discount     = models.DecimalField(
                     max_digits=5,
                     decimal_places=2,
                     validators=[
                         MinValueValidator(0.01),
                         MaxValueValidator(100)
                     ]
                   )
    discountType = models.CharField(
                     max_length=20,
                     choices=DISCOUNT_TYPES
                   )
    startDate    = models.DateField()
    endDate      = models.DateField()
    status       = models.CharField(
                     max_length=20,
                     default='active',
                     choices=[('active', 'Active'), ('inactive', 'Inactive')]
                   )
    created      = models.DateTimeField(auto_now_add=True)
    modified     = models.DateTimeField(auto_now=True)
    created_id   = models.ForeignKey(
                     Users,
                     on_delete=models.SET_NULL,
                     null=True, blank=True,
                     related_name='promotions_created'
                   )
    modified_id  = models.ForeignKey(
                     Users,
                     on_delete=models.SET_NULL,
                     null=True, blank=True,
                     related_name='promotions_modified'
                   )

    class Meta:
        db_table = 'promotions'
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'

    def clean(self):
        validate_end_date(self)

    def __str__(self):
        return self.name


# =========================================================
# PRODUCTS_PROMOTIONS
# =========================================================
class ProductsPromotions(models.Model):
    product     = models.ForeignKey(
                    Products,
                    on_delete=models.CASCADE,
                    related_name='promotions'
                  )
    promotion   = models.ForeignKey(
                    Promotions,
                    on_delete=models.CASCADE,
                    related_name='products'
                  )
    status      = models.CharField(
                    max_length=20,
                    default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')]
                  )
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    created_id  = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='products_promotions_created'
                  )
    modified_id = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='products_promotions_modified'
                  )

    class Meta:
        db_table = 'products_promotions'
        verbose_name = 'Product Promotion'
        verbose_name_plural = 'Products Promotions'
        unique_together = ('product', 'promotion')

    def __str__(self):
        return f"{self.product.name} - {self.promotion.name}"


# =========================================================
# LOCATIONS
# =========================================================
class Locations(models.Model):
    user        = models.ForeignKey(
                    Users,
                    on_delete=models.CASCADE,
                    related_name='locations'
                  )
    alias       = models.CharField(max_length=100, blank=True, null=True)
    address     = models.CharField(
                    max_length=255,
                    validators=[validate_not_blank]
                  )
    reference   = models.TextField(blank=True, null=True)
    isDefault   = models.BooleanField(default=False)
    status      = models.CharField(
                    max_length=20,
                    default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')]
                  )
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    created_id  = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='locations_created'
                  )
    modified_id = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='locations_modified'
                  )

    class Meta:
        db_table = 'locations'
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return self.address


# =========================================================
# ORDERS
# =========================================================
class Orders(models.Model):
    ORDER_STATUS = [
        ('pending',   'Pending'),
        ('preparing', 'Preparing'),
        ('ready',     'Ready'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user        = models.ForeignKey(
                    Users,
                    on_delete=models.CASCADE,
                    related_name='orders'
                  )
    location    = models.ForeignKey(
                    Locations,
                    on_delete=models.PROTECT,
                    related_name='orders'
                  )
    orderStatus = models.CharField(
                    max_length=20,
                    choices=ORDER_STATUS,
                    default='pending'
                  )
    total       = models.DecimalField(
                    max_digits=10,
                    decimal_places=2,
                    validators=[MinValueValidator(0)]
                  )
    notes       = models.TextField(blank=True, null=True)
    status      = models.CharField(
                    max_length=20,
                    default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')]
                  )
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    created_id  = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='orders_created'
                  )
    modified_id = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='orders_modified'
                  )

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"


# =========================================================
# ORDER_DETAILS
# =========================================================
class OrderDetails(models.Model):
    order       = models.ForeignKey(
                    Orders,
                    on_delete=models.CASCADE,
                    related_name='details'
                  )
    product     = models.ForeignKey(
                    Products,
                    on_delete=models.PROTECT,
                    related_name='order_details'
                  )
    quantity    = models.IntegerField(
                    validators=[MinValueValidator(1)]
                  )
    unitPrice   = models.DecimalField(
                    max_digits=10,
                    decimal_places=2,
                    validators=[MinValueValidator(0.01)]
                  )
    subtotal    = models.DecimalField(
                    max_digits=10,
                    decimal_places=2,
                    validators=[MinValueValidator(0)]
                  )
    status      = models.CharField(
                    max_length=20,
                    default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')]
                  )
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    created_id  = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='order_details_created'
                  )
    modified_id = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='order_details_modified'
                  )

    class Meta:
        db_table = 'order_details'
        verbose_name = 'Order Detail'
        verbose_name_plural = 'Order Details'
        unique_together = ('order', 'product')

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unitPrice
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order.id} - {self.product.name}"


# =========================================================
# DRIVERS
# =========================================================
class Drivers(models.Model):
    user        = models.OneToOneField(
                    Users,
                    on_delete=models.CASCADE,
                    related_name='driver'
                  )
    license     = models.CharField(
                    max_length=50,
                    unique=True,
                    validators=[validate_not_blank]
                  )
    phone       = models.CharField(
                    max_length=20,
                    blank=True, null=True,
                    validators=[MinLengthValidator(7)]
                  )
    status      = models.CharField(
                    max_length=20,
                    default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')]
                  )
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    created_id  = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='drivers_created'
                  )
    modified_id = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='drivers_modified'
                  )

    class Meta:
        db_table = 'drivers'
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'

    def __str__(self):
        return f"{self.user.firstName} {self.user.lastName}"


# =========================================================
# VEHICLES
# =========================================================
class Vehicles(models.Model):
    driver      = models.ForeignKey(
                    Drivers,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='vehicles'
                  )
    plate       = models.CharField(
                    max_length=20,
                    unique=True,
                    validators=[validate_not_blank]
                  )
    model       = models.CharField(
                    max_length=100,
                    validators=[validate_not_blank]
                  )
    status      = models.CharField(
                    max_length=20,
                    default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')]
                  )
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    created_id  = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='vehicles_created'
                  )
    modified_id = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='vehicles_modified'
                  )

    class Meta:
        db_table = 'vehicles'
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'

    def __str__(self):
        return f"{self.plate} - {self.model}"


# =========================================================
# DELIVERIES
# =========================================================
class Deliveries(models.Model):
    DELIVERY_STATUS = [
        ('pending',    'Pending'),
        ('on_the_way', 'On The Way'),
        ('delivered',  'Delivered'),
        ('failed',     'Failed'),
    ]

    order          = models.OneToOneField(
                       Orders,
                       on_delete=models.CASCADE,
                       related_name='delivery'
                     )
    driver         = models.ForeignKey(
                       Drivers,
                       on_delete=models.SET_NULL,
                       null=True, blank=True,
                       related_name='deliveries'
                     )
    vehicle        = models.ForeignKey(
                       Vehicles,
                       on_delete=models.SET_NULL,
                       null=True, blank=True,
                       related_name='deliveries'
                     )
    deliveryStatus = models.CharField(
                       max_length=20,
                       choices=DELIVERY_STATUS,
                       default='pending'
                     )
    departureAt    = models.DateTimeField(blank=True, null=True)
    deliveredAt    = models.DateTimeField(blank=True, null=True)
    status         = models.CharField(
                       max_length=20,
                       default='active',
                       choices=[('active', 'Active'), ('inactive', 'Inactive')]
                     )
    created        = models.DateTimeField(auto_now_add=True)
    modified       = models.DateTimeField(auto_now=True)
    created_id     = models.ForeignKey(
                       Users,
                       on_delete=models.SET_NULL,
                       null=True, blank=True,
                       related_name='deliveries_created'
                     )
    modified_id    = models.ForeignKey(
                       Users,
                       on_delete=models.SET_NULL,
                       null=True, blank=True,
                       related_name='deliveries_modified'
                     )

    class Meta:
        db_table = 'deliveries'
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'

    def clean(self):
        validate_delivery_dates(self)

    def __str__(self):
        return f"Delivery - Order #{self.order.id}"


# =========================================================
# REVIEWS
# =========================================================
class Reviews(models.Model):
    user        = models.ForeignKey(
                    Users,
                    on_delete=models.CASCADE,
                    related_name='reviews'
                  )
    product     = models.ForeignKey(
                    Products,
                    on_delete=models.CASCADE,
                    related_name='reviews'
                  )
    rating      = models.SmallIntegerField(
                    validators=[
                        MinValueValidator(1),
                        MaxValueValidator(5)
                    ]
                  )
    comment     = models.TextField(blank=True, null=True)
    status      = models.CharField(
                    max_length=20,
                    default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')]
                  )
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    created_id  = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='reviews_created'
                  )
    modified_id = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='reviews_modified'
                  )

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.rating}★)"


# =========================================================
# MESSAGES
# =========================================================
class Messages(models.Model):
    user        = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='messages'
                  )
    subject     = models.CharField(
                    max_length=150,
                    validators=[validate_not_blank]
                  )
    body        = models.TextField(
                    validators=[validate_not_blank]
                  )
    isRead      = models.BooleanField(default=False)
    status      = models.CharField(
                    max_length=20,
                    default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')]
                  )
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    created_id  = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='messages_created'
                  )
    modified_id = models.ForeignKey(
                    Users,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='messages_modified'
                  )

    class Meta:
        db_table = 'messages'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return self.subject