from rest_framework.routers import DefaultRouter
from .views import MenuCategoryViewSet, MenuItemViewSet

router = DefaultRouter()
router.register(r'categories', MenuCategoryViewSet, basename='menu-category')
router.register(r'items', MenuItemViewSet, basename='menu-item')

urlpatterns = router.urls
