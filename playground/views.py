from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.db.models.functions import Concat

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

    # queryset = Product.objects.defer('description')

    # *Selecting Related Tables:
    # queryset = Product.objects.select_related('collection').all()

    # *Aggregation:
    # result = Product.objects.aggregate(
    #     count=Count('id'), min_price=Min('unit_price'))

    # *How many orders do we have?
    # result = Order.objects.aggregate(total_orders=Count('id'))

    # *How many units of product 1 have we sold?
    # result = OrderItem.objects.filter(product_id=1).aggregate(
    #     total_units_sold=Sum('quantity'))

    # *How many orders has customer 1 placed?
    # result = Order.objects.filter(customer_id=1).aggregate(Count('id'))

    # *What is the min, max and average price of the products in collection 3?
    # result = Product.objects.filter(
    #     collection_id=3).aggregate(min=Min('unit_price'), max=Max('unit_price'), avg=Avg('unit_price'))

    # *Annotate
    # queryset = Customer.objects.annotate(is_new=Value(True))
    # queryset = Customer.objects.annotate(new_id=F('id')+1)

    # *Calling Database functions:
    # queryset = Customer.objects.annotate(
    #     # CONCAT
    #     full_name=Func(F('first_name'), Value(
    #         " "), F('last_name'), function='CONCAT')
    # )

    # queryset = Customer.objects.annotate(fullname=Concat('first_name', Value(" "), 'last_name')
    #                                      )

    # queryset = Customer.objects.annotate(
    #     orders_count=Count('order')
    # )

    # *Expression Wrapper
    # queryset = Product.objects.annotate(
    #     discounted_price=ExpressionWrapper(
    #         F('unit_price') * 0.8, output_field=DecimalField())
    # )

    # *Customers with their last order id:
    # queryset = Customer.objects.annotate(last_order=Max('order'))

    # *Collections and count of their products:
    # queryset = Collection.objects.annotate(
    #     total_products=Count('product')
    # )

    # *Customers with more than 5 orders
    # queryset = Customer.objects.annotate(
    #     total_orders=Count('order__id')
    # ).filter(total_orders__gt=5)

    # *Customers and the total amount they’ve spent
    # queryset = Customer.objects.annotate(
    #     amount_spent=Sum(
    #         F('order__orderitem__unit_price') * F('order__orderitem__quantity')
    #     )
    # )

    # *Top 5 best-selling products and their total sales:
    # queryset = Product.objects.annotate(
    #     total_sales=Sum(F('orderitem__quantity') * F('orderitem__unit_price'))
    # ).order_by('-total_sales')[:5]

    # *Insert:
    # coll = Collection()
    # coll.title = 'Video Games'
    # coll.featured_product = Product(pk=1)
    # coll.save()

    # or
    # Collection.objects.create(title = '')

    # *Update
    # coll = Collection(pk=11)
    # # coll.title = 'Games'
    # coll.featured_product = None
    # coll.save()

    # coll = Collection.objects.get(pk=11)
    # # coll.title = 'Video Games'
    # coll.featured_product = None
    # coll.save()

    # or
    # Collection.objects.filter(pk=11).update(featured_product_id=1)

    # *Delete:
    Collection.objects.filter(id__gt=10).delete()

    return render(req, 'hello.html', {'name': 'Gaurav'})
