from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Reviews(models.Model):
    # 1. ID principal explícito requerido por la rúbrica y tu DER
    id          = models.AutoField(primary_key=True)
    
    # 2. Relaciones corregidas (Nombre limpio en Python, columnas exactas del DER en la BD)
    user        = models.ForeignKey('api.Users', on_delete=models.CASCADE, related_name='reviews', db_column='user_id')
    product     = models.ForeignKey('api.Products', on_delete=models.CASCADE, related_name='reviews', db_column='product_id')
    
    rating      = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment     = models.TextField(blank=True, null=True)
    status      = models.CharField(max_length=20, default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    
    # 3. Campos de auditoría forzados para la BD según el DER
    created_id  = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews_created', db_column='created_id')
    modified_id = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews_modified', db_column='modified_id')

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        # Restricción de unicidad usando las variables limpias de Python
        unique_together = ('user', 'product')

    def save(self, *args, **kwargs):
        # Asegurar que se ejecuten las restricciones del rango de calificación (1-5)
        self.clean_fields()
        
        # Limpiar espacios del comentario
        if self.comment:
            self.comment = self.comment.strip()
            
        super().save(*args, **kwargs)

    def __str__(self):
        user_display = self.user.email if self.user else "Anonymous"
        product_display = self.product.name if self.product else "No Product"
        return f"{user_display} - {product_display} ({self.rating}★)"