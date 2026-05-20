from django.db import models
from django.core.validators import MinValueValidator


class Inventories(models.Model):
    # 1. ID principal explícito requerido por la rúbrica
    id          = models.AutoField(primary_key=True)
    
    # 2. Relación corregida (Nombre limpio en Python, columna exacta del DER en la BD)
    product     = models.OneToOneField('api.Products', on_delete=models.CASCADE, related_name='inventory', db_column='product_id')
    
    stock       = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    minStock    = models.IntegerField(default=5, validators=[MinValueValidator(0)])
    status      = models.CharField(max_length=20, default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    
    # 3. Campos de auditoría forzados para la BD según el DER
    created_id  = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='inventories_created', db_column='created_id')
    modified_id = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='inventories_modified', db_column='modified_id')

    class Meta:
        db_table = 'inventories'
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'

    def save(self, *args, **kwargs):
        # Asegurar que se ejecuten las restricciones del MinValueValidator
        self.clean_fields()
        
        # Si el stock llega a 0 o menos, asegurar que no sea negativo e inactivar
        if self.stock is not None and self.stock <= 0:
            self.stock  = 0
            self.status = 'inactive'
        else:
            self.status = 'active'
            
        super().save(*args, **kwargs)

    def __str__(self):
        # Acceso natural al nombre del producto a través del ORM
        product_name = self.product.name if self.product else "No Product"
        return f"{product_name} - Stock: {self.stock} (Min: {self.minStock})"