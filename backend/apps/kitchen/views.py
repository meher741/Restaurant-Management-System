from rest_framework import viewsets, permissions
from .models import KitchenTicket
from .serializers import KitchenTicketSerializer

class KitchenTicketViewSet(viewsets.ModelViewSet):
    queryset = KitchenTicket.objects.all()
    serializer_class = KitchenTicketSerializer
    permission_classes = [permissions.IsAuthenticated]
