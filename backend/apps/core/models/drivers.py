from django.db import models
from django.core.validators import MinLengthValidator
from .validators import validate_not_blank


class Drivers(models.Model):
    # 1. ID principal explícito requerido por la rúbrica
    id          = models.AutoField(primary_key=True)
    
    # 2. Relación corregida (Nombre limpio en Python, columna exacta del DER en la BD)
    user        = models.OneToOneField('Users', on_delete=models.CASCADE, related_name='driver', db_column='user_id')
    
    license     = models.CharField(max_length=50, unique=True, validators=[validate_not_blank])
    phone       = models.CharField(max_length=20, blank=True, null=True, validators=[MinLengthValidator(7)])
    status      = models.CharField(max_length=20, default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    
    # 3. Campos de auditoría forzados para la BD
    created_id  = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='drivers_created', db_column='created_id')
    modified_id = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='drivers_modified', db_column='modified_id')

    class Meta:
        db_table = 'drivers'
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'

    def save(self, *args, **kwargs):
        # Ejecuta las restricciones de los atributos individuales de forma segura
        self.clean_fields()
        
        # Normalizar licencia a mayúsculas
        if self.license:
            self.license = self.license.strip().upper()
            
        super().save(*args, **kwargs)

    def __str__(self):
        # Acceso directo al objeto relacionado 'user'
        user_display = f"{self.user.firstName} {self.user.lastName}" if self.user else "No User"
        return f"{user_display} - {self.license}"