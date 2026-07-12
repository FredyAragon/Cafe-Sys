from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from .models import Categories, Locations, OrderDetails, Orders, Products


@override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}})
class OrderCreationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='order@example.com',
            password='secret123',
            firstName='Order',
            lastName='User',
            role='Customer',
            is_staff=False,
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
        self.location = Locations.objects.create(
            user=self.user,
            address='Av. Test 123',
            created_id=self.user,
            modified_id=self.user,
        )

    def test_create_order_with_details_succeeds(self):
        response = self.client.post('/apps/core/orders/', {
            'user': self.user.id,
            'location': self.location.id,
            'orderStatus': 'pending',
            'total': '5.00',
            'notes': 'Prueba de pedido',
            'details_data': [{
                'product': self.product.id,
                'quantity': 2,
                'unitPrice': '2.50'
            }]
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Orders.objects.count(), 1)
        self.assertEqual(OrderDetails.objects.count(), 1)
        detail = OrderDetails.objects.get(order_id=response.data['id'])
        self.assertEqual(str(detail.subtotal), '5.00')


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
