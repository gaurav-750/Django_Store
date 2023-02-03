from django.urls import path, include
from .views import product_list, product_detail

urlpatterns = [
    path('products/', product_list),
    path('products/<int:pk>', product_detail)
]
