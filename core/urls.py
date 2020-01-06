from django.urls import path
from .views import (HomeView, checkout, ItemDetailView, OrderSummaryView, add_to_cart, remove_from_cart)


app_name = "core"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("checkout/", checkout, name="checkout"),
    path("order-summary/", OrderSummaryView.as_view(), name="order-summary"),
    path("product/<int:pk>/", ItemDetailView.as_view(), name="product"),
    path("add-to-cart/<int:pk>/", add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<int:pk>/", remove_from_cart, name="remove-from-cart"),
]