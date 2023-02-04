from django.urls import path, include
# from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

from .views import ProductViewSet, CollectionViewset, ReviewViewset

router = routers.DefaultRouter()
# Parent router
router.register('products', ProductViewSet)

products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
# Child router
products_router.register('reviews', ReviewViewset, basename='product-reviews')

router.register('collections', CollectionViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
]
