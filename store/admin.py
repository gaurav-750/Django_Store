from django.contrib import admin
from django.db.models.aggregates import Count

from .models import Collection, Product, Customer, Order

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'unit_price',
                    'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_per_page = 20
    ordering = ['id']

    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        else:
            return 'Ok'


admin.site.register(Product, ProductAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10


admin.site.register(Customer, CustomerAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    # ordering = ['id']


admin.site.register(Order, OrderAdmin)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='total_products_count')
    def products_count(self, collection):
        return collection.total_products_count

    def get_queryset(self, request):
        return Collection.objects.annotate(
            total_products_count=Count('product')
        )

# admin.site.register(Collection)
