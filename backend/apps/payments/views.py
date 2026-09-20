from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Payment, Invoice
from .serializers import PaymentSerializer, InvoiceSerializer
from .services import PaymentProcessingService, BillingService
from apps.orders.models import Order
from django.shortcuts import get_object_or_404

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['ADMIN', 'MANAGER']:
            return Payment.objects.all()
        return Payment.objects.filter(order__customer=user)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order = serializer.validated_data['order']
        amount = serializer.validated_data['amount']
        payment_method = serializer.validated_data['payment_method']
        transaction_id = serializer.validated_data.get('transaction_id')
        
        # We process the payment using our service instead of directly saving
        try:
            payment = PaymentProcessingService.process_payment(order, amount, payment_method, transaction_id)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def refund(self, request, pk=None):
        payment = self.get_object()
        
        # Only admin or manager can refund
        if request.user.role not in ['ADMIN', 'MANAGER']:
            return Response({'detail': 'You do not have permission to refund payments.'}, status=status.HTTP_403_FORBIDDEN)
            
        try:
            refunded_payment = PaymentProcessingService.refund_payment(payment)
            return Response(PaymentSerializer(refunded_payment).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['ADMIN', 'MANAGER']:
            return Invoice.objects.all()
        return Invoice.objects.filter(customer=user)
        
    @action(detail=False, methods=['post'], url_path='generate/(?P<order_id>[^/.]+)')
    def generate(self, request, order_id=None):
        order = get_object_or_404(Order, pk=order_id)
        
        # Check permissions
        if request.user.role not in ['ADMIN', 'MANAGER'] and order.customer != request.user:
            return Response({'detail': 'You do not have permission to access this order.'}, status=status.HTTP_403_FORBIDDEN)
            
        # Optional: ensure BillingService is run first
        BillingService.calculate_order_totals(order)
        invoice = BillingService.generate_invoice(order)
        
        return Response(InvoiceSerializer(invoice).data, status=status.HTTP_201_CREATED)
