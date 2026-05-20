from django.db import models
from .validators import validate_not_blank


class Locations(models.Model):
    # 1. ID principal explícito requerido por la rúbrica
    id          = models.AutoField(primary_key=True)
    
    # 2. Relación corregida (Nombre limpio en Python, columna exacta del DER en la BD)
    user        = models.ForeignKey('api.Users', on_delete=models.CASCADE, related_name='locations', db_column='user_id')
    
    alias       = models.CharField(max_length=100, blank=True, null=True)
    address     = models.CharField(max_length=255, validators=[validate_not_blank])
    reference   = models.TextField(blank=True, null=True)
    isDefault   = models.BooleanField(default=False)
    status      = models.CharField(max_length=20, default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    
    # 3. Campos de auditoría forzados para la BD según el DER
    created_id  = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='locations_created', db_column='created_id')
    modified_id = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='locations_modified', db_column='modified_id')

    class Meta:
        db_table = 'locations'
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def save(self, *args, **kwargs):
        # Ejecuta las restricciones de los atributos individuales (como validate_not_blank)
        self.clean_fields()
        
        # Normalizar dirección
        if self.address:
            self.address = self.address.strip()
            
        # Si no hay alias, usar los primeros 30 caracteres de la dirección ya limpia
        if not self.alias and self.address:
            self.alias = self.address[:30]
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.alias} - {self.address}"