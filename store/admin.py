from django.contrib import admin
from .models import Collection, Product, Customer


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'unit_price']
    list_editable = ['unit_price']
    list_per_page = 20
    ordering = ['id']


admin.site.register(Product, ProductAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10


admin.site.register(Customer, CustomerAdmin)


admin.site.register(Collection)
