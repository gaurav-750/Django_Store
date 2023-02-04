from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter

from .views import ProductViewSet, CollectionViewset

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('collections', CollectionViewset)

urlpatterns = [
    path('', include(router.urls))
]
