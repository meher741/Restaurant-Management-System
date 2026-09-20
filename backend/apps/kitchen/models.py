from django.db import models
from apps.restaurants.models import Restaurant
from apps.orders.models import Order

class KitchenTicket(models.Model):
    class TicketStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PREPARING = 'PREPARING', 'Preparing'
        READY = 'READY', 'Ready'
        SERVED = 'SERVED', 'Served'
        CANCELLED = 'CANCELLED', 'Cancelled'

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='kitchen_tickets')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='kitchen_tickets')
    status = models.CharField(max_length=20, choices=TicketStatus.choices, default=TicketStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'kitchen_tickets'
        ordering = ['created_at']

    def __str__(self):
        return f"Ticket #{self.id} for Order #{self.order.id} - {self.status}"
