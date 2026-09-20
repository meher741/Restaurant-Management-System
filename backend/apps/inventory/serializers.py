from rest_framework import serializers
from .models import Ingredient, InventoryTransaction

class InventoryTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTransaction
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    transactions = InventoryTransactionSerializer(many=True, read_only=True)
    is_low_stock = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = '__all__'

    def get_is_low_stock(self, obj):
        return obj.current_stock <= obj.reorder_level
