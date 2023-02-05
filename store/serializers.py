from decimal import Decimal
from rest_framework import serializers

from .models import CartItem, Product, Collection, Review, Cart


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


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']

    # title = serializers.CharField(read_only=True)
    # unit_price = serializers.DecimalField(
    #     max_digits=6, decimal_places=2, read_only=True)


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField('get_total_price')

    def get_total_price(self, cart_item: CartItem):
        return cart_item.product.unit_price * cart_item.quantity

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    cartitems = CartItemSerializer(many=True, read_only=True)

    total_amount = serializers.SerializerMethodField('get_total_amount')

    def get_total_amount(self, cart: Cart):
        amount = 0
        items = CartItem.objects.filter(cart_id=cart.id)
        for item in list(items):
            amount += item.product.unit_price * item.quantity
        return amount

    class Meta:
        model = Cart
        fields = ['id', 'cartitems', 'total_amount']
