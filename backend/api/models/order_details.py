from django.db import models
from django.core.validators import MinValueValidator


class OrderDetails(models.Model):
    # 1. ID principal explícito requerido por la rúbrica y tu DER
    id          = models.AutoField(primary_key=True)
    
    # 2. Relaciones corregidas (Nombre limpio en Python, columnas exactas del DER en la BD)
    order       = models.ForeignKey('api.Orders', on_delete=models.CASCADE, related_name='details', db_column='order_id')
    product     = models.ForeignKey('api.Products', on_delete=models.PROTECT, related_name='order_details', db_column='product_id')
    
    quantity    = models.IntegerField(validators=[MinValueValidator(1)])
    unitPrice   = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    subtotal    = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status      = models.CharField(max_length=20, default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    
    # 3. Campos de auditoría forzados para la BD según el DER
    created_id  = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='order_details_created', db_column='created_id')
    modified_id = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='order_details_modified', db_column='modified_id')

    class Meta:
        db_table = 'order_details'
        verbose_name = 'Order Detail'
        verbose_name_plural = 'Order Details'
        # Unicidad usando los nombres de las propiedades en Python
        unique_together = ('order', 'product')

    def save(self, *args, **kwargs):
        # Asegurar que se ejecuten las restricciones de cantidad y precio
        self.clean_fields()
        
        # Calcular subtotal automáticamente de forma segura
        if self.quantity is not None and self.unitPrice is not None:
            self.subtotal = round(self.quantity * float(self.unitPrice), 2)
            
        super().save(*args, **kwargs)

    def __str__(self):
        order_display = self.order.id if self.order else "None"
        product_display = self.product.name if self.product else "No Product"
        return f"Order #{order_display} - {product_display} x{self.quantity} = S/. {self.subtotal}"