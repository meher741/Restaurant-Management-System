from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()


class NotificationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@test.com",
            password="password",
            first_name="Test",
            last_name="User",
        )
        self.notification = Notification.objects.create(
            user=self.user, title="Test", message="Test message"
        )
        self.client.force_authenticate(user=self.user)

    def test_list_notifications(self):
        response = self.client.get("/api/notifications/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_mark_read(self):
        response = self.client.patch(f"/api/notifications/{self.notification.id}/read/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

    def test_read_all(self):
        Notification.objects.create(user=self.user, title="Test 2", message="Msg 2")
        response = self.client.post("/api/notifications/read-all/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Notification.objects.filter(is_read=False).count(), 0)
