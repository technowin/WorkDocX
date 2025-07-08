from django.urls import path

from .views import (products_view, products_details_view, orders_view, order_details_view, customers_view, shopping_cart_view, checkout_view, sellers_view )

app_name = "ecommerce"
urlpatterns = [
    path("products", view=products_view, name="products"),
    path("products-details", view=products_details_view, name="products-details"),
    path("orders", view=orders_view, name="orders"),
    path("order-details", view=order_details_view, name="order-details"),
    path("customers", view=customers_view, name="customers"),
    path("shopping-cart", view=shopping_cart_view, name="shopping-cart"),
    path("checkout", view=checkout_view, name="checkout"),
    path("sellers", view=sellers_view, name="sellers")
]
