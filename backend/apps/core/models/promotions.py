from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from .validators import validate_not_blank, validate_end_date, validate_http_url


class Promotions(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed',      'Fixed Amount'),
    ]

    id           = models.AutoField(primary_key=True)
    name         = models.CharField(max_length=150, validators=[validate_not_blank])
    description  = models.TextField(blank=True, null=True)
    
    discount     = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    discountType = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    
    imageUrl     = models.CharField(max_length=255, blank=True, null=True, validators=[validate_http_url])

    startDate    = models.DateField(null=True, blank=True)
    endDate      = models.DateField(null=True, blank=True)
    status       = models.CharField(max_length=20, default='active', choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created      = models.DateTimeField(auto_now_add=True)
    modified     = models.DateTimeField(auto_now=True)
    
    created_id   = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='promotions_created', db_column='created_id')
    modified_id  = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='promotions_modified', db_column='modified_id')

    class Meta:
        db_table = 'promotions'
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'

    def save(self, *args, **kwargs):
        self.clean_fields()
        self.clean()  # Ejecuta las validaciones cruzadas antes de guardar
        
        if self.endDate and self.endDate < timezone.now().date():
            self.status = 'inactive'
        elif not self.endDate:
            # Sin fecha de fin, la promoción permanece activa
            self.status = self.status or 'active'
            
        super().save(*args, **kwargs)

    def clean(self):
        # 1. Tu validación existente para las fechas
        if self.startDate and self.endDate:
            validate_end_date(self)

        # 2. Validar que la fecha de inicio no sea posterior a la de fin
        if self.startDate and self.endDate and self.startDate > self.endDate:
            raise ValidationError({'endDate': 'La fecha de fin no puede ser anterior a la de inicio.'})

        # 3. NUEVA VALIDACIÓN DINÁMICA: Valida el 100% solo si es porcentaje
        if self.discountType == 'percentage' and self.discount > 100:
            raise ValidationError({'discount': 'Un descuento porcentual no puede ser mayor al 100%.'})
