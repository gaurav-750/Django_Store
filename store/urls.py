from django.urls import path, include
from .views import ProductList, ProductDetail, collection_list, collection_detail

urlpatterns = [
    path('products/', ProductList.as_view()),
    path('products/<int:pk>', ProductDetail.as_view()),
    path('collections/', collection_list),
    path('collections/<int:pk>/', collection_detail, name='collection-detail'),
]
