from locust import HttpUser, task, between
from random import randint


class WebsiteUser(HttpUser):
    # locust will randomly wait between 1 to 5 secs between each task
    wait_time = between(1, 5)

    @task
    def say_hello(self):
        self.client.get(
            '/playground/hello/',
            name='hello'
        )

    # viewing products
    @task(2)  # weight -> kitni chances hai ye endpt.pe user jane k
    def view_products(self):
        collection_id = randint(3, 6)
        self.client.get(
            f'/store/products/?collection_id={collection_id}',
            name='/store/products'
        )

    # viewing a particular product:
    @task(4)  # that means a user is twice likely to view a part.prod that all
    def view_product(self):
        product_id = randint(1, 1000)
        self.client.get(
            f'/store/products/{product_id}/',
            name='/store/products/:id'
        )

    # adding a product to cart:
    @task(1)
    def add_to_cart(self):
        product_id = randint(1, 10)
        self.client.post(
            f'/store/carts/{self.cart_id}/cartitems/',
            name='store/carts/cartitems',
            json={  # to send the data
                'product_id': product_id,
                'quantity': 1
            }
        )

    # *This fn is called everytime a new user is on our website
    # here we'll create a cart for the user
    def on_start(self):
        res = self.client.post('/store/carts/')
        result = res.json()
        self.cart_id = result['id']
