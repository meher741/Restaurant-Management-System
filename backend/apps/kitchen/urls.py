from rest_framework.routers import DefaultRouter
from .views import KitchenTicketViewSet

router = DefaultRouter()
router.register(r'tickets', KitchenTicketViewSet, basename='kitchen-ticket')

urlpatterns = router.urls
