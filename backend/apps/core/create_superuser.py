import os
import sys
import django

sys.path.append('/app')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafesys.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

user, created = User.objects.get_or_create(
    email='admin@cafesys.com',
    defaults={
        'firstName': 'Admin',
        'lastName': 'Sistema',
        'is_staff': True,
        'is_superuser': True,
        'is_active': True,
        'role': 'Admin',
    }
)

if created:
    user.set_password('admin1234')
    user.save()
    print('Superusuario creado: admin@cafesys.com / admin1234')
else:
    user.set_password('admin1234')
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.role = 'Admin'
    user.firstName = 'Admin'
    user.lastName = 'Sistema'
    user.save()
    print('Superusuario actualizado: admin@cafesys.com / admin1234')