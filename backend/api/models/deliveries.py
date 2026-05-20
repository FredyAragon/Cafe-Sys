from django.db import models
from django.utils import timezone
from .validators import validate_delivery_dates


class Deliveries(models.Model):
    DELIVERY_STATUS = [
        ('pending',    'Pending'),
        ('on_the_way', 'On The Way'),
        ('delivered',  'Delivered'),
        ('failed',     'Failed'),
    ]

    # 1. ID principal explícito requerido por la rúbrica
    id = models.AutoField(primary_key=True)

    # 2. Relaciones corregidas (Nombre limpio en Python, nombre exacto del DER en PostgreSQL)
    order   = models.OneToOneField('api.Orders', on_delete=models.CASCADE, related_name='delivery', db_column='order_id')
    driver  = models.ForeignKey('api.Drivers', on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries', db_column='driver_id')
    vehicle = models.ForeignKey('api.Vehicles', on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries', db_column='vehicle_id')
    
    deliveryStatus = models.CharField(max_length=20, choices=DELIVERY_STATUS, default='pending')
    departureAt    = models.DateTimeField(blank=True, null=True)
    deliveredAt    = models.DateTimeField(blank=True, null=True)
    
    status         = models.CharField(max_length=20, default='active',
                               choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created        = models.DateTimeField(auto_now_add=True)
    modified       = models.DateTimeField(auto_now=True)
    
    # 3. Auditoría forzada para cumplir con el DER sin duplicar el "_id_id"
    created_id     = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries_created', db_column='created_id')
    modified_id    = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries_modified', db_column='modified_id')

    class Meta:
        db_table = 'deliveries'
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'

    def save(self, *args, **kwargs):
        # Ejecuta validaciones de atributos (campos individuales)
        self.clean_fields()
        # Llama a tu función clean() personalizada (validate_delivery_dates)
        self.clean()
        
        # Registrar fecha de entrega automáticamente al marcar como delivered
        if self.deliveryStatus == 'delivered' and not self.deliveredAt:
            self.deliveredAt = timezone.now()
            
        # Si falla, marcar como inactivo    
        if self.deliveryStatus == 'failed':
            self.status = 'inactive'
            
        super().save(*args, **kwargs)

    def clean(self):
        # Corre tu validador personalizado de fechas
        validate_delivery_dates(self)

    def __str__(self):
        # Ahora accedemos de forma natural y pitónica a través de 'self.order'
        order_display = self.order.id if self.order else "None"
        return f"Delivery #{self.id} - Order #{order_display} | {self.deliveryStatus}"