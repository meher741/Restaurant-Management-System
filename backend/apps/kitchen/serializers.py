from rest_framework import serializers
from .models import KitchenTicket

class KitchenTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenTicket
        fields = '__all__'
