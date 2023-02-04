from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework import status

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


# Create your views here.
class ProductList(APIView):
    def get(self, req):
        products = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            products, many=True, context={
                'request': req,
            })
        return Response(serializer.data)

    def post(self, req):
        # deserialization
        serializer = ProductSerializer(data=req.data)
        # *validate the data:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, req, pk):
        product = get_object_or_404(Product, pk=pk)
        # it'll convert our product obj into dictionary
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, req, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, req, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitem_set.count() > 0:
            return Response({"error": "Order items are related to this product"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def collection_list(req):
    if req.method == 'GET':
        collections = Collection.objects.annotate(
            products_count=Count('products'))
        serializer = CollectionSerializer(collections, many=True)

        return Response(serializer.data)
    elif req.method == 'POST':
        # deserialization
        serializer = CollectionSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(req, pk):
    collection = get_object_or_404(Collection.objects.annotate(
        products_count=Count('products')), pk=pk)
    if req.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif req.method == 'PUT':
        serializer = CollectionSerializer(collection, data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    elif req.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({"error": "Products are related to this collection!"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def product_list(req):
#     if req.method == 'GET':

#     elif req.method == 'POST':

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(req, pk):
#     if req.method == 'GET':

#     elif req.method == 'PUT':

#     elif req.method == 'DELETE':
