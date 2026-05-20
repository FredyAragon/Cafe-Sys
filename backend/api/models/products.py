from django.db import models
from django.core.validators import MinValueValidator
from .validators import validate_not_blank, validate_http_url


class Products(models.Model):
    # 1. ID principal explícito requerido por la rúbrica y tu DER
    id          = models.AutoField(primary_key=True)
    
    name        = models.CharField(max_length=150, validators=[validate_not_blank])
    description = models.TextField(blank=True, null=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    imageUrl    = models.CharField(max_length=255, blank=True, null=True, validators=[validate_http_url])
    
    # 2. Relación corregida (Nombre limpio en Python, columna exacta del DER en la BD)
    category    = models.ForeignKey('api.Categories', on_delete=models.PROTECT, related_name='products', db_column='category_id')
    
    status      = models.CharField(max_length=20, default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    
    # 3. Campos de auditoría forzados para la BD según el DER
    created_id  = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='products_created', db_column='created_id')
    modified_id = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='products_modified', db_column='modified_id')

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        # Asegurar que se ejecuten las restricciones de los atributos individuales
        self.clean_fields()
        
        # Normalizar nombre con capitalización
        if self.name:
            self.name = self.name.strip().title()
            
        # Redondear precio a 2 decimales
        if self.price is not None:
            self.price = round(self.price, 2)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - S/. {self.price}"