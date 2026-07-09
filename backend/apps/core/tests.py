from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from .models import Categories, Locations, OrderDetails, Orders, Products


@override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}})
class ProductsDeletionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='admin@example.com',
            password='secret123',
            firstName='Admin',
            lastName='User',
            role='Admin',
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

        self.category = Categories.objects.create(
            name='Bebidas',
            description='Categoría de prueba',
            status='active',
            created_id=self.user,
            modified_id=self.user,
        )
        self.product = Products.objects.create(
            name='Café',
            description='Producto de prueba',
            price='2.50',
            category=self.category,
            status='active',
            created_id=self.user,
            modified_id=self.user,
        )

    def test_delete_product_removes_it_when_it_has_order_details(self):
        location = Locations.objects.create(
            user=self.user,
            address='Av. Test 123',
            created_id=self.user,
            modified_id=self.user,
        )
        order = Orders.objects.create(
            user=self.user,
            location=location,
            total='2.50',
            created_id=self.user,
            modified_id=self.user,
        )
        OrderDetails.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            unitPrice='2.50',
            subtotal='2.50',
            created_id=self.user,
            modified_id=self.user,
        )

        response = self.client.delete(f'/apps/core/products/{self.product.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Products.objects.filter(pk=self.product.pk).exists())
        self.assertFalse(OrderDetails.objects.filter(product_id=self.product.pk).exists())
