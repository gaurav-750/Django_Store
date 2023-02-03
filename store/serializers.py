from decimal import Decimal
from rest_framework import serializers

from .models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'price_with_tax', 'collection']

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(
    #     source='unit_price', max_digits=5, decimal_places=2)

    # # adding custom field:
    price_with_tax = serializers.SerializerMethodField(method_name='cal_tax')

    # # *Serializing relationships:
    # # collection = serializers.PrimaryKeyRelatedField(
    # #     queryset=Collection.objects.all()
    # # )
    # collection = serializers.StringRelatedField()

    # # collection = CollectionSerializer()
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )

    def cal_tax(self, product: Product):
        return round(product.unit_price * Decimal(1.1), ndigits=2)
