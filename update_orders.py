import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from apps.orders.models import Order
orders = Order.objects.all()
for order in orders:
    order.subtotal = order.total_amount
    order.discount_amount = 0
    order.tax_amount = 0
    order.save()
print(f'Updated {len(orders)} orders')
