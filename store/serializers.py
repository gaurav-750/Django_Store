from decimal import Decimal
from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(
        source='unit_price', max_digits=5, decimal_places=2)

    # adding custom field:
    price_with_tax = serializers.SerializerMethodField(method_name='cal_tax')

    def cal_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
