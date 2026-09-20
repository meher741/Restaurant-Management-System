from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.restaurants.models import Restaurant, Table
from .models import Order
from decimal import Decimal

User = get_user_model()

class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@test.com', password='password', first_name='Test')
        self.restaurant = Restaurant.objects.create(
            name='Test Rest', address='123', city='City', state='State',
            postal_code='123', phone='123', email='r@r.com',
            opening_time='09:00:00', closing_time='22:00:00'
        )
        self.table = Table.objects.create(restaurant=self.restaurant, table_number=1, capacity=4)
        
        self.order = Order.objects.create(
            customer=self.user,
            restaurant=self.restaurant,
            table=self.table,
            subtotal=Decimal('100.00'),
            discount_amount=Decimal('0.00'),
            tax_amount=Decimal('5.00'),
            total_amount=Decimal('105.00')
        )
        
    def test_list_orders(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['total_amount'], '105.00')
