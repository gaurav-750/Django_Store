from decimal import Decimal
from rest_framework import serializers

from .models import Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory',
                  'unit_price', 'price_with_tax', 'collection']

    # *adding custom field:
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


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        # validated_data -> form se aa raha hai, and usme hum product_id add kr rahe
        return Review.objects.create(product_id=product_id, **validated_data)
