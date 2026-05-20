from django.db import models
from django.core.validators import MinLengthValidator
from .validators import validate_not_blank


class Users(models.Model):
    # 1. ID principal explícito requerido por la rúbrica y tu DER
    id           = models.AutoField(primary_key=True)
    
    firstName    = models.CharField(max_length=100, validators=[validate_not_blank])
    lastName     = models.CharField(max_length=100, validators=[validate_not_blank])
    email        = models.EmailField(unique=True)
    passwordHash = models.CharField(max_length=255, validators=[MinLengthValidator(8)])
    
    # 2. Relación corregida (Nombre limpio en Python, columna exacta del DER en la BD)
    role         = models.ForeignKey('api.Roles', on_delete=models.PROTECT, related_name='users', db_column='role_id')
    
    status       = models.CharField(max_length=20, default='active',
                     choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created      = models.DateTimeField(auto_now_add=True)
    modified     = models.DateTimeField(auto_now=True)
    
    # 3. Campos de auditoría forzados para la BD según el DER
    created_id   = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='users_created', db_column='created_id')
    modified_id  = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='users_modified', db_column='modified_id')

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def save(self, *args, **kwargs):
        # Asegurar que se ejecuten las restricciones de los atributos individuales
        self.clean_fields()
        
        # Normalizar email a minúsculas antes de guardar
        if self.email:
            self.email = self.email.lower().strip()
            
        # Normalizar nombre con capitalización
        if self.firstName:
            self.firstName = self.firstName.strip().title()
        if self.lastName:
            self.lastName  = self.lastName.strip().title()
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.firstName} {self.lastName} ({self.email})"