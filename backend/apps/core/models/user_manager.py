from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        # Importamos dinámicamente el modelo Roles para evitar importaciones circulares
        from apps.core.models.roles import Roles

        # Buscamos o creamos el rol 'Administrador' en la base de datos local
        rol_admin, _ = Roles.objects.get_or_create(
            name="Administrador",
            defaults={"description": "Superusuario del sistema con todos los permisos"}
        )

        # Asignamos la llave foránea al diccionario de campos extra
        extra_fields.setdefault("role", rol_admin)

        return self.create_user(
            email=email,
            password=password,
            **extra_fields
        )