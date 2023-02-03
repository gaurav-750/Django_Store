from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.status import HTTP_404_NOT_FOUND

from .models import Product
from .serializers import ProductSerializer


# Create your views here.
@api_view()
def product_list(req):
    products = Product.objects.select_related('collection').all()
    serializer = ProductSerializer(
        products, many=True, context={
            'request': req,
        })

    return Response(serializer.data)


@api_view()
def product_detail(req, pk):
    product = get_object_or_404(Product, pk=pk)
    # it'll convert our product obj into dictionary
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view()
def collection_detail(req, pk):
    return Response("ok")
