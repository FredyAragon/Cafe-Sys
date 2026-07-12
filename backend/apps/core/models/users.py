from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)
from .validators import validate_not_blank
from .user_manager import UserManager


class Users(AbstractBaseUser, PermissionsMixin):
    id          = models.AutoField(primary_key=True)

    firstName   = models.CharField(max_length=100, validators=[validate_not_blank])
    lastName    = models.CharField(max_length=100, validators=[validate_not_blank])
    email       = models.EmailField(unique=True)

    ROLE_CHOICES = [
        ('Admin', 'Administrator'),
        ('Driver', 'Driver'),
        ('Customer', 'Customer'),
        ('Employee', 'Employee'),
    ]
    role        = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Customer')

    is_staff    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)

    status      = models.CharField(max_length=20, default='active',
                                   choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)

    created_id  = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='users_created', db_column='created_id')
    modified_id = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True, blank=True, related_name='users_modified', db_column='modified_id')

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ["firstName", "lastName"]

    objects = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def save(self, *args, **kwargs):
        self.clean_fields()

        if self.email:
            self.email = self.email.lower().strip()

        if self.firstName:
            self.firstName = self.firstName.strip().title()
        if self.lastName:
            self.lastName  = self.lastName.strip().title()

        # Auto-set is_staff based on role
        self.is_staff = self.role in ('Admin', 'Employee', 'Driver')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.firstName} {self.lastName} ({self.email})"