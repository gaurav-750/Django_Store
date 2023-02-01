from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F

from store.models import Product, Customer, Collection, Order, OrderItem

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
    # queryset = Product.objects.filter(inventory=F('unit_price'))

    # queryset = Product.objects.order_by('title')
    # queryset = Product.objects.order_by('unit_price', '-title')

    # queryset = Product.objects.all()[0:5]

    # queryset = Product.objects.values('id', 'title', 'collection__title')

    # *Customers with .com accounts:
    # queryset = Customer.objects.filter(email__endswith='.com')

    # *Collections that don’t have a featured product:
    # queryset = Collection.objects.filter(featured_product_id__isnull=True)

    # *Products with low inventory (less than 10)
    # queryset = Product.objects.filter(inventory__lt=10)

    # *Orders placed by customer with id = 1
    # queryset = Order.objects.filter(customer_id=1)

    # *Order items for products in collection 3
    # queryset = OrderItem.objects.filter(product__collection_id=3)

    return render(req, 'hello.html', {'name': 'Gaurav', 'result': list(queryset)})
