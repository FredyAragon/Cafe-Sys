from django.db import models
from .validators import validate_not_blank, validate_http_url


class Categories(models.Model):
    # 1. ID principal explícito como pide la recomendación
    id          = models.AutoField(primary_key=True)
    
    name        = models.CharField(max_length=100, unique=True, validators=[validate_not_blank])
    description = models.TextField(blank=True, null=True)
    imageUrl    = models.CharField(max_length=255, blank=True, null=True, validators=[validate_http_url])
    status      = models.CharField(max_length=20, default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    
    # 2. Forzar el nombre de la columna en la BD para cumplir con la rúbrica y evitar el "_id_id"
    created_id  = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='categories_created', db_column='created_id')
    modified_id = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='categories_modified', db_column='modified_id')

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        # CORRECCIÓN: Ejecuta los validadores personalizados de tus atributos sin romper el flujo del Admin
        self.clean_fields()
        
        # Normalizar nombre con capitalización
        if self.name:
            self.name = self.name.strip().title()
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name