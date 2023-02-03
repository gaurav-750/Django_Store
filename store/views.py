from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer


# Create your views here.
@api_view(['GET', 'POST'])
def product_list(req):
    if req.method == 'GET':
        products = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            products, many=True, context={
                'request': req,
            })

        return Response(serializer.data)
    elif req.method == 'POST':
        # deserialization
        serializer = ProductSerializer(data=req.data)
        print(type(serializer))

        # *validate the data:
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(req, pk):
    product = get_object_or_404(Product, pk=pk)
    if req.method == 'GET':
        # it'll convert our product obj into dictionary
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif req.method == 'PUT':
        serializer = ProductSerializer(product, data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif req.method == 'DELETE':
        if product.orderitem_set.count() > 0:
            return Response({"error": "Order items are related to this product"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def collection_detail(req, pk):
    return Response("ok")
