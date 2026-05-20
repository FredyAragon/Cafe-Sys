from django.db import models
from .validators import validate_not_blank


class Messages(models.Model):
    # 1. ID principal explícito requerido por la rúbrica
    id          = models.AutoField(primary_key=True)
    
    # 2. Relación corregida (Nombre limpio en Python, columna exacta del DER en la BD)
    user        = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='messages', db_column='user_id')
    
    subject     = models.CharField(max_length=150, validators=[validate_not_blank])
    body        = models.TextField(validators=[validate_not_blank])
    isRead      = models.BooleanField(default=False)
    status      = models.CharField(max_length=20, default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    
    # 3. Campos de auditoría forzados para la BD según el DER
    created_id  = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='messages_created', db_column='created_id')
    modified_id = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='messages_modified', db_column='modified_id')

    class Meta:
        db_table = 'messages'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def save(self, *args, **kwargs):
        # Asegurar que se ejecuten las restricciones de no estar en blanco
        self.clean_fields()
        
        # Normalizar asunto con capitalización
        if self.subject:
            self.subject = self.subject.strip().capitalize()
            
        # Limpiar espacios del cuerpo
        if self.body:
            self.body = self.body.strip()
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject} ({'Leído' if self.isRead else 'No leído'})"