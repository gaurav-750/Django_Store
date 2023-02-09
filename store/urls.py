from django.urls import path, include
# from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

from .views import OrderViewset, ProductViewSet, CollectionViewset, ReviewViewset, CustomerViewset, CartViewset, CartItemViewset

router = routers.DefaultRouter()
# Parent router
router.register('products', ProductViewSet, basename='products')
router.register('collections', CollectionViewset)
router.register('carts', CartViewset)
router.register('customers', CustomerViewset)
router.register('orders', OrderViewset, basename='orders')

# Child router
products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', ReviewViewset, basename='product-reviews')

carts_router = routers.NestedDefaultRouter(
    router, 'carts', lookup='cart')
carts_router.register('cartitems', CartItemViewset,
                      basename='cart-cartitems')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(carts_router.urls)),
]
