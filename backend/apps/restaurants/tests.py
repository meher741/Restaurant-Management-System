from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Restaurant, Table

User = get_user_model()

class RestaurantTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(email='admin@test.com', password='password', first_name='Admin')
        self.restaurant = Restaurant.objects.create(
            name='Test Rest', address='123 Main', city='City', state='State',
            postal_code='12345', phone='1234567890', email='rest@test.com',
            opening_time='09:00:00', closing_time='22:00:00'
        )
        self.table = Table.objects.create(restaurant=self.restaurant, table_number=1, capacity=4)
        
    def test_list_restaurants(self):
        response = self.client.get('/api/restaurants/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Rest')
        
    def test_list_tables(self):
        response = self.client.get(f'/api/restaurants/{self.restaurant.id}/tables/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['table_number'], 1)
