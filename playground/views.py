from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from store.models import Product

# Create your views here.


def say_hello(req):

    # query_set = Product.objects.filter(pk=0).first()
    # print(query_set)

    # queryset = Product.objects.filter(title__contains='coffee')
    # queryset = Product.objects.filter(title__icontains='coffee')
    queryset = Product.objects.filter(last_update__year=2021)
    print('QSET:', queryset)

    return render(req, 'hello.html', {'name': 'Gaurav', 'result': list(queryset)})
