from django.urls import path
from .views import HomeView, checkout, ItemDetailView, add_to_cart


app_name = "core"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("checkout/", checkout, name="checkout"),
    path("product/<int:pk>", ItemDetailView.as_view(), name="product"),
    path("add-to-cart<int:pk>", add_to_cart, name="add-to-cart"),
]
