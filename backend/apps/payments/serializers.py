from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("paid_at", "created_at")
    
    def validate_amount(self, value):
        """Validate that amount is greater than zero"""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
    
    def validate(self, attrs):
        """Validate that payment amount matches order total amount"""
        amount = attrs.get("amount")
        order = attrs.get("order")
        
        if order and amount is not None:
            if amount != order.total_amount:
                raise serializers.ValidationError({
                    "amount": f"Payment amount ({amount}) does not match order total amount ({order.total_amount})."
                })
        return attrs

from .models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ("invoice_number", "created_at", "subtotal", "discount_amount", "tax_amount", "total_amount", "items_summary")
