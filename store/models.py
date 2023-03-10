from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

from uuid import uuid4

from .validators import validate_file_size


# Create your models here.
class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Product(models.Model):
    title = models.CharField(max_length=255)  # varchar(255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2,
                                     validators=[MinValueValidator(1)]
                                     )
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)

    # *1-Many
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')

    # many-many
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='store/images',
                              validators=[validate_file_size]
                              )
    # image will be stored in /media/store/images/


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    # in the product class, we;d have an attribute names 'reviews'
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]

    #! first_name, last_name, email exists in User model also. So, no need to define it here.
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

    # choice field
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    # *1-1 (Customer - User)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    # *1-Many (1 Customer -> Many addresses)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETED = 'C'
    PAYMENT_FAILED = 'F'
    PAYMENT_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETED, 'Completed'),
        (PAYMENT_FAILED, 'Failed'),
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_CHOICES, default=PAYMENT_PENDING)

    # *1-Many
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    # *1-Many
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    # *1-Many
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cartitems')
    # so in Cart we'll have 'cartitems' instead of cartitem_set
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveSmallIntegerField()

    # *create a unique index on cart+product
    class Meta:
        unique_together = [['cart', 'product']]
