from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F

from store.models import Product

# Create your views here.


def say_hello(req):

    # query_set = Product.objects.filter(pk=0).first()
    # print(query_set)

    # queryset = Product.objects.filter(title__contains='coffee')
    # queryset = Product.objects.filter(title__icontains='coffee')
    # queryset = Product.objects.filter(last_update__year=2021)

    # *Products: inventory < 10 AND price < 20
    # queryset = Product.objects.filter(
    # inventory__lt=10).filter(unit_price__lt=20)

    # *Products: inventory < 10 OR price < 20
    # queryset = Product.objects.filter(
    #     Q(inventory__lt=10) | Q(unit_price__lt=20))

    # *Products: inventory = unit_price
    queryset = Product.objects.filter(inventory=F('unit_price'))

    return render(req, 'hello.html', {'name': 'Gaurav', 'result': list(queryset)})
