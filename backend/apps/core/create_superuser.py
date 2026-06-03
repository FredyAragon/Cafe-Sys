import os
import sys
import django

sys.path.append('/app')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafesys.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(email='admin@cafesys.com').exists():
    User.objects.create_superuser(
        email='admin@cafesys.com',
        password='admin1234',
        firstName='Admin',
        lastName='Sistema'
    )
    print('Superusuario creado: admin@cafesys.com / admin1234')
else:
    print('Superusuario ya existe')