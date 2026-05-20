from django.db import models
from django.core.validators import MinValueValidator


class Orders(models.Model):
    ORDER_STATUS = [
        ('pending',   'Pending'),
        ('preparing', 'Preparing'),
        ('ready',     'Ready'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    # 1. ID principal explícito requerido por la rúbrica y tu DER
    id          = models.AutoField(primary_key=True)

    # 2. Relaciones corregidas (Nombre limpio en Python, columnas exactas del DER en la BD)
    user        = models.ForeignKey('api.Users', on_delete=models.CASCADE, related_name='orders', db_column='user_id')
    location    = models.ForeignKey('api.Locations', on_delete=models.PROTECT, related_name='orders', db_column='location_id')
    
    orderStatus = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    total       = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    notes       = models.TextField(blank=True, null=True)
    status      = models.CharField(max_length=20, default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    
    # 3. Campos de auditoría forzados para la BD según el DER
    created_id  = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders_created', db_column='created_id')
    modified_id = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders_modified', db_column='modified_id')

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def save(self, *args, **kwargs):
        # Asegurar que se ejecuten las restricciones del validador de total
        self.clean_fields()
        
        # Si el pedido es cancelado, marcarlo como inactivo
        if self.orderStatus == 'cancelled':
            self.status = 'inactive'
            
        # Redondear total
        if self.total is not None:
            self.total = round(self.total, 2)
            
        super().save(*args, **kwargs)

    def __str__(self):
        user_display = f"{self.user.firstName} {self.user.lastName}" if self.user else "No User"
        return f"Order #{self.id} | {user_display} | {self.orderStatus} | S/. {self.total}"