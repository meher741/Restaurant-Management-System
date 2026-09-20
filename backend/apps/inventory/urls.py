from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet, InventoryTransactionViewSet

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'transactions', InventoryTransactionViewSet, basename='inventory-transaction')

urlpatterns = router.urls
