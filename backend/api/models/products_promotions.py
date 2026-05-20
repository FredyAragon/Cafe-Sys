from django.db import models
from django.utils import timezone


class ProductsPromotions(models.Model):
    # 1. ID principal explícito requerido por la rúbrica y tu DER
    id          = models.AutoField(primary_key=True)
    
    # 2. Relaciones corregidas (Nombre limpio en Python, columnas exactas del DER en la BD)
    product     = models.ForeignKey('api.Products', on_delete=models.CASCADE, related_name='product_promotions', db_column='product_id')
    promotion   = models.ForeignKey('api.Promotions', on_delete=models.CASCADE, related_name='product_promotions', db_column='promotion_id')
    
    status      = models.CharField(max_length=20, default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    
    # 3. Campos de auditoría forzados para la BD según el DER
    created_id  = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='products_promotions_created', db_column='created_id')
    modified_id = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='products_promotions_modified', db_column='modified_id')

    class Meta:
        db_table = 'products_promotions'
        verbose_name = 'Product Promotion'
        verbose_name_plural = 'Products Promotions'
        # Unicidad usando las propiedades limpias en Python
        unique_together = ('product', 'promotion')

    def save(self, *args, **kwargs):
        # Asegurar la validación segura de campos
        self.clean_fields()
        
        # Si la promoción asociada existe y está inactiva, desactivar también esta relación
        if self.promotion and self.promotion.status == 'inactive':
            self.status = 'inactive'
            
        super().save(*args, **kwargs)

    def __str__(self):
        product_display = self.product.name if self.product else "No Product"
        promotion_display = self.promotion.name if self.promotion else "No Promotion"
        return f"{product_display} - {promotion_display}"