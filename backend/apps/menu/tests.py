from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.restaurants.models import Restaurant
from .models import MenuCategory, MenuItem

User = get_user_model()

class MenuTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(email='admin@test.com', password='password', first_name='Admin')
        self.restaurant = Restaurant.objects.create(
            name='Test Rest', address='123', city='City', state='State',
            postal_code='123', phone='123', email='r@r.com',
            opening_time='09:00:00', closing_time='22:00:00'
        )
        self.category = MenuCategory.objects.create(restaurant=self.restaurant, name='Drinks')
        self.item = MenuItem.objects.create(category=self.category, name='Cola', price='2.50')
        
    def test_list_menu_items(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/menu/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Cola')
