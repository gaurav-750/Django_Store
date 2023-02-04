from django.urls import path, include
from .views import ProductList, ProductDetail, CollectionList, collection_detail

urlpatterns = [
    path('products/', ProductList.as_view()),
    path('products/<int:pk>', ProductDetail.as_view()),
    path('collections/', CollectionList.as_view()),
    path('collections/<int:pk>/', collection_detail, name='collection-detail'),
]
