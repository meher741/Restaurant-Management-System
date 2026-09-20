import uuid
from django.utils import timezone
from decimal import Decimal
from django.db import transaction
from .models import Payment, Invoice
from apps.orders.models import Order


class BillingService:
    @staticmethod
    def calculate_order_totals(
        order, discount=Decimal("0.00"), tax_rate=Decimal("0.05")
    ):
        """
        Calculates subtotal, discount, tax, and total amount for an order.
        Since we lack OrderItem right now, we assume subtotal is provided or previously computed.
        """
        subtotal = order.subtotal or Decimal("0.00")
        tax_amount = round((subtotal - discount) * tax_rate, 2)
        total_amount = round(subtotal - discount + tax_amount, 2)

        order.discount_amount = round(discount, 2)
        order.tax_amount = tax_amount
        order.total_amount = total_amount
        order.save()

        return order

    @staticmethod
    @transaction.atomic
    def generate_invoice(order):
        """
        Generates an invoice for a given order.
        """
        if hasattr(order, "invoice"):
            return order.invoice

        invoice_number = (
            f"INV-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        )

        # Determine items summary (placeholder until OrderItems are implemented)
        items_summary = [
            {
                "name": "Order items summary",
                "quantity": 1,
                "unit_price": float(order.subtotal),
                "total": float(order.subtotal),
            }
        ]

        invoice = Invoice.objects.create(
            invoice_number=invoice_number,
            order=order,
            restaurant=order.restaurant,
            customer=order.customer,
            items_summary=items_summary,
            subtotal=order.subtotal,
            discount_amount=order.discount_amount,
            tax_amount=order.tax_amount,
            total_amount=order.total_amount,
            payment_status=order.payment_status,
        )
        return invoice


class PaymentProcessingService:
    @staticmethod
    @transaction.atomic
    def process_payment(order, amount, payment_method, transaction_id=None):
        """
        Processes a payment for an order and syncs statuses.
        """
        # Check if already paid
        if order.payment_status == Order.PaymentStatus.SUCCESS:
            raise ValueError("Order is already paid.")

        # Create payment record
        payment = Payment.objects.create(
            order=order,
            amount=amount,
            payment_method=payment_method,
            transaction_id=transaction_id,
            status=Payment.PaymentStatus.SUCCESS,
            paid_at=timezone.now(),
        )

        # Sync order payment status
        order.payment_status = Order.PaymentStatus.SUCCESS
        order.save()

        # Update invoice if exists
        if hasattr(order, "invoice"):
            order.invoice.payment_method = payment_method
            order.invoice.payment_status = Payment.PaymentStatus.SUCCESS
            order.invoice.save()

        return payment

    @staticmethod
    @transaction.atomic
    def refund_payment(payment):
        """
        Refunds a successful payment.
        """
        if payment.status != Payment.PaymentStatus.SUCCESS:
            raise ValueError("Only successful payments can be refunded.")

        payment.status = Payment.PaymentStatus.REFUNDED
        payment.save()

        # We don't mark the order as PENDING automatically, it could be cancelled or refunded
        order = payment.order
        order.payment_status = Order.PaymentStatus.REFUNDED
        order.save()

        if hasattr(order, "invoice"):
            order.invoice.payment_status = Payment.PaymentStatus.REFUNDED
            order.invoice.save()

        return payment
