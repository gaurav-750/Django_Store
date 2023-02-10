from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import CartItem, Customer, Order, OrderItem, Product, Collection, Review, Cart


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


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField('get_total_price')

    def get_total_price(self, cart_item: CartItem):
        return cart_item.product.unit_price * cart_item.quantity

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        try:
            product = Product.objects.get(pk=value)
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError(
                'No product with this ID exists!')

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)

            # cartitem exists: Update the cartitem
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            # create a new cart item
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


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


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at',
                  'payment_status', 'orderitems']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    # todo validate the cart_id (whether it exists or not)
    def validate_cart_id(self, cart_id):
        # if the cart does not exists (means the cart_id is wrong)
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError(
                "Cart with this id does not exists!")

        # if the cart is empty: in this case, we do not want to create an order:
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError("The cart is empty.")
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']

            (customer, created) = Customer.objects.get_or_create(
                user_id=self.context['user_id'])
            # todo create an Order:
            order_created = Order.objects.create(customer_id=customer.id)

            # todo OrderItems:
            # for each cartitem in the Cart, we need to create an order item and save it in the db:
            cart_items = CartItem.objects.select_related('product').filter(
                cart_id=cart_id)

            # using list comprehension:
            order_items = [
                OrderItem(
                    order=order_created,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity
                ) for item in cart_items
            ]

            # *save the order_items in the DB:
            OrderItem.objects.bulk_create(order_items)

            # delete the cart:
            Cart.objects.filter(pk=cart_id).delete()
            return order_created
