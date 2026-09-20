from django.db import models
from apps.users.models import User

class Notification(models.Model):
    class NotificationType(models.TextChoices):
        ORDER = 'ORDER', 'Order'
        RESERVATION = 'RESERVATION', 'Reservation'
        PAYMENT = 'PAYMENT', 'Payment'
        INVENTORY = 'INVENTORY', 'Inventory'
        SYSTEM = 'SYSTEM', 'System'
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices, default=NotificationType.SYSTEM)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        
    def __str__(self):
        return f'{self.title} - {self.user.email}'
