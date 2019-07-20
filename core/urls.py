from django.urls import path
from . import views as myviews


app_name = 'core'
urlpatterns = [
    path('', myviews.home, name='home'),
    path('product/', myviews.product, name='product'),
    path('checkout/', myviews.checkout, name='checkout'),
]
