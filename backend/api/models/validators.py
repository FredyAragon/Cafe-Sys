from django.core.exceptions import ValidationError

def validate_not_blank(value):
    if not value or not value.strip():
        raise ValidationError('This field cannot be blank or whitespace.')

def validate_http_url(value):
    if value and not value.startswith('http'):
        raise ValidationError('URL must start with http or https.')

def validate_end_date(instance):
    if instance.endDate and instance.startDate:
        if instance.endDate < instance.startDate:
            raise ValidationError('End date must be greater than or equal to start date.')

def validate_delivery_dates(instance):
    if instance.deliveredAt and instance.departureAt:
        if instance.deliveredAt < instance.departureAt:
            raise ValidationError('Delivered date cannot be before departure date.')