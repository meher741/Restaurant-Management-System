from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.restaurants.models import Restaurant, Table
from apps.orders.models import Order
from apps.payments.models import Payment, Invoice
from apps.payments.services import BillingService, PaymentProcessingService
from decimal import Decimal

User = get_user_model()

class PaymentBillingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = User.objects.create_user(email='cust@test.com', password='password', role='CUSTOMER', first_name='Cust', last_name='Test')
        self.admin = User.objects.create_superuser(email='admin@test.com', password='password', first_name='Admin', last_name='Test')
        
        self.restaurant = Restaurant.objects.create(
            name='Test Rest', address='123 Main', city='City', state='State',
            postal_code='12345', phone='1234567890', email='rest@test.com',
            opening_time='09:00:00', closing_time='22:00:00'
        )
        self.table = Table.objects.create(restaurant=self.restaurant, table_number=1, capacity=4)
        
        self.order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            table=self.table,
            subtotal=Decimal('1000.00'),
            discount_amount=Decimal('0.00'),
            tax_amount=Decimal('0.00'),
            total_amount=Decimal('1000.00')
        )
        
    def test_billing_service_calculate(self):
        BillingService.calculate_order_totals(self.order, discount=Decimal('100.00'), tax_rate=Decimal('0.10'))
        self.order.refresh_from_db()
        # Subtotal: 1000, discount: 100. Tax = 900 * 0.10 = 90. Total = 1000 - 100 + 90 = 990
        self.assertEqual(self.order.total_amount, Decimal('990.00'))
        
    def test_payment_processing(self):
        payment = PaymentProcessingService.process_payment(
            order=self.order,
            amount=Decimal('1000.00'),
            payment_method='CARD'
        )
        self.assertEqual(payment.status, Payment.PaymentStatus.SUCCESS)
        self.order.refresh_from_db()
        self.assertEqual(self.order.payment_status, Order.PaymentStatus.SUCCESS)
        
    def test_payment_processing_already_paid(self):
        self.order.payment_status = Order.PaymentStatus.SUCCESS
        self.order.save()
        with self.assertRaises(ValueError):
            PaymentProcessingService.process_payment(
                order=self.order,
                amount=Decimal('1000.00'),
                payment_method='CARD'
            )
            
    def test_refund_payment(self):
        payment = PaymentProcessingService.process_payment(
            order=self.order,
            amount=Decimal('1000.00'),
            payment_method='CARD'
        )
        PaymentProcessingService.refund_payment(payment)
        self.order.refresh_from_db()
        self.assertEqual(payment.status, Payment.PaymentStatus.REFUNDED)
        self.assertEqual(self.order.payment_status, Order.PaymentStatus.REFUNDED)
        
    def test_generate_invoice(self):
        invoice = BillingService.generate_invoice(self.order)
        self.assertEqual(invoice.order, self.order)
        self.assertEqual(invoice.total_amount, Decimal('1000.00'))
