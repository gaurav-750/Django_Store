from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

from .models import Collection, Product, Customer, Order

# Register your models here.


class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'unit_price',
                    'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_per_page = 20
    list_filter = ['collection', 'last_update', InventoryFilter]

    ordering = ['id']

    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        else:
            return 'Ok'


admin.site.register(Product, ProductAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'myorders']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    def myorders(self, customer):
        url = (reverse('admin:store_order_changelist')
               + "?" +
               urlencode({
                   'customer_id': str(customer.id)
               })
               )
        return format_html('<a href="{}"> {}  </a>', url, 'myorders')


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
        url = (reverse('admin:store_product_changelist')
               + "?" +
               urlencode({
                   'collection__id': str(collection.id)
               })
               )
        return format_html('<a href="{}"> {}  </a>', url, collection.total_products_count)

    def get_queryset(self, request):
        return Collection.objects.annotate(
            total_products_count=Count('product')
        )

# admin.site.register(Collection)
