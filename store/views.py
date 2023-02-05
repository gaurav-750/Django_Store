from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status

from .models import Product, Collection, OrderItem, Review, Cart, CartItem
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from .filters import ProductFilter
from .pagination import CustomPagination

# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = Product.objects.filter(collection_id=collection_id)

    #     return queryset

    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id', 'unit_price']
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    pagination_class = CustomPagination

    def get_serializer_context(self):
        return {
            'request': self.request,
        }

    def destroy(self, request, *args, **kwargs):
        print(kwargs)
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({"error": "Order items are related to this product"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ReviewViewset(ModelViewSet):
    # queryset = Review.objects.all()
    def get_queryset(self):
        # self.kwargs = {'product_pk': '2'}
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    serializer_class = ReviewSerializer

    # todo To pass some extra data to serializer
    def get_serializer_context(self):
        return {
            'product_id': self.kwargs['product_pk']
        }


class CollectionViewset(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')
    )
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({"error": "Products are related to this collection!"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class CartViewset(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('cartitems__product').all()
    serializer_class = CartSerializer


class CartItemViewset(ModelViewSet):
    # *only this methods will be allowed at this endpoint
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        else:
            return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}


# class ProductList(ListCreateAPIView):
#     queryset = Product.all()
#     serializer_class = ProductSerializer

#     # def get_queryset(self):
#     # return Product.objects.select_related('collection').all()

#     # def get_serializer_class(self):
#     #     return ProductSerializer

#     def get_serializer_context(self):
#         return {
#             'request': self.request,
#         }

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     # queryset = Product.objects.all()
#     # serializer_class = ProductSerializer

#     def delete(self, req, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitem_set.count() > 0:
#             return Response({"error": "Order items are related to this product"},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(
#         products_count=Count('products')
#     )

#     serializer_class = CollectionSerializer

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     # GET, PUT
#     queryset = Collection.objects.annotate(products_count=Count('products'))
#     serializer_class = CollectionSerializer

#     def delete(self, req, pk):
#         collection = get_object_or_404(Collection, pk=pk)
#         if collection.products.count() > 0:
#             return Response({"error": "Products are related to this collection!"},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)

#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
