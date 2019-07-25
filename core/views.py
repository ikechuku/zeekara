from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Item, Order, OrderItem


def products(request):
    context = {"items": Item.objects.all()}
    return render(request, "product-page.html", context)


def checkout(request):
    context = {"items": Item.objects.all()}
    return render(request, "checkout-page.html", context)


class HomeView(ListView):
    model = Item
    template_name = "home-page.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item = OrderItem.objects.create(item=item)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        # check if the ordered item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()

    else:
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)

    return redirect("core:product", kwargs={"pk": pk})

