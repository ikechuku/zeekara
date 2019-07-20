from django.shortcuts import render
from .models import Item

def home(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'home-page.html', context)


def product(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'product-page.html', context)



def checkout(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'checkout-page.html', context)
