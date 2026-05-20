from django.db import models
from .validators import validate_not_blank


class Vehicles(models.Model):
    # 1. ID principal explícito requerido por la rúbrica y tu DER
    id          = models.AutoField(primary_key=True)
    
    # 2. Relación corregida (Nombre limpio en Python, columna exacta del DER en la BD)
    driver      = models.ForeignKey('api.Drivers', on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicles', db_column='driver_id')
    
    plate       = models.CharField(max_length=20, unique=True, validators=[validate_not_blank])
    model       = models.CharField(max_length=100, validators=[validate_not_blank])
    status      = models.CharField(max_length=20, default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    
    # 3. Campos de auditoría forzados para la BD según el DER
    created_id  = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicles_created', db_column='created_id')
    modified_id = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicles_modified', db_column='modified_id')

    class Meta:
        db_table = 'vehicles'
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'

    def save(self, *args, **kwargs):
        # Asegurar que se ejecuten las restricciones de los atributos individuales
        self.clean_fields()
        
        # Normalizar placa a mayúsculas sin espacios
        if self.plate:
            self.plate = self.plate.strip().upper().replace(' ', '')
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.plate} - {self.model}"