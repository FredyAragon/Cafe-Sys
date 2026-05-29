from django.db import models
from .validators import validate_not_blank


class Roles(models.Model):
    # 1. ID principal explícito requerido por la rúbrica y tu DER
    id          = models.AutoField(primary_key=True)
    
    name        = models.CharField(max_length=50, unique=True, validators=[validate_not_blank])
    description = models.TextField(blank=True, null=True)
    status      = models.CharField(max_length=20, default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    
    # 2. Campos de auditoría forzados para la BD según el DER
    created_id  = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='roles_created', db_column='created_id')
    modified_id = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='roles_modified', db_column='modified_id')

    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def save(self, *args, **kwargs):
        # Asegurar la ejecución segura de los validadores de atributos individuales
        self.clean_fields()
        
        # Normalizar nombre a minúsculas
        if self.name:
            self.name = self.name.strip().lower()
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name