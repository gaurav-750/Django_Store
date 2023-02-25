from django.urls import path
from .views import say_hello, HelloView


urlpatterns = [
    path('hello/', HelloView.as_view())
]
