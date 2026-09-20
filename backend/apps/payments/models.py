from django.db import models
from django.core.validators import MinValueValidator
from apps.orders.models import Order

class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'CASH', 'Cash'
        CARD = 'CARD', 'Card'
        UPI = 'UPI', 'UPI'
        ONLINE = 'ONLINE', 'Online'
    
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'
        REFUNDED = 'REFUNDED', 'Refunded'
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices)
    status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Payment #{self.id} for Order #{self.order.id} - {self.status}'

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='invoices')
    customer = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='invoices')
    
    # Store item snapshot as a JSON field since order items might change or be deleted
    # Example format: [{"name": "Item 1", "quantity": 2, "unit_price": 250, "total": 500}]
    items_summary = models.JSONField(default=list)
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    payment_method = models.CharField(max_length=10, choices=Payment.PaymentMethod.choices, blank=True, null=True)
    payment_status = models.CharField(max_length=10, choices=Payment.PaymentStatus.choices, default=Payment.PaymentStatus.PENDING)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'invoices'
        ordering = ['-created_at']
        
    def __str__(self):
        return f'Invoice {self.invoice_number} for Order #{self.order.id}'
