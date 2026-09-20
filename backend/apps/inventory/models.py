from django.db import models
from apps.restaurants.models import Restaurant
from apps.menu.models import MenuItem

class Ingredient(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=100)
    unit_of_measurement = models.CharField(max_length=50) # e.g., kg, liters, units
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    reorder_level = models.DecimalField(max_digits=10, decimal_places=2, default=10.0)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    last_restocked = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ingredients'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.current_stock} {self.unit_of_measurement})"

class InventoryTransaction(models.Model):
    class TransactionType(models.TextChoices):
        RESTOCK = 'RESTOCK', 'Restock'
        USAGE = 'USAGE', 'Usage'
        SPOILAGE = 'SPOILAGE', 'Spoilage'
        ADJUSTMENT = 'ADJUSTMENT', 'Adjustment'

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'inventory_transactions'
        ordering = ['-transaction_date']

    def __str__(self):
        return f"{self.transaction_type} of {self.quantity} for {self.ingredient.name}"
