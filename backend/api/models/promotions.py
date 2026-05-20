from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from .validators import validate_not_blank, validate_end_date


class Promotions(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed',      'Fixed Amount'),
    ]

    # 1. ID principal explícito requerido por la rúbrica y tu DER
    id           = models.AutoField(primary_key=True)

    name         = models.CharField(max_length=150, validators=[validate_not_blank])
    description  = models.TextField(blank=True, null=True)
    discount     = models.DecimalField(max_digits=5, decimal_places=2,
                     validators=[MinValueValidator(0.01), MaxValueValidator(100)])
    discountType = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    startDate    = models.DateField()
    endDate      = models.DateField()
    status       = models.CharField(max_length=20, default='active',
                     choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created      = models.DateTimeField(auto_now_add=True)
    modified     = models.DateTimeField(auto_now=True)
    
    # 2. Campos de auditoría forzados para la BD según el DER
    created_id   = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='promotions_created', db_column='created_id')
    modified_id  = models.ForeignKey('api.Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='promotions_modified', db_column='modified_id')

    class Meta:
        db_table = 'promotions'
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'

    def save(self, *args, **kwargs):
        # Ejecutar restricciones de atributos individuales
        self.clean_fields()
        # Ejecutar la validación personalizada de fechas (validate_end_date)
        self.clean()
        
        # Si la fecha de fin ya pasó, desactivar automáticamente
        if self.endDate and self.endDate < timezone.now().date():
            self.status = 'inactive'
            
        super().save(*args, **kwargs)

    def clean(self):
        # Llama a tu función que valida que la fecha de fin sea posterior a la de inicio
        validate_end_date(self)

    def __str__(self):
        return f"{self.name} - {self.discount}{'%' if self.discountType == 'percentage' else ' S/.'}"