from django.shortcuts import render
from .models import Item

def homepage(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'home-page.html', context)


def checkout(check)