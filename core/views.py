from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Item, Order, OrderItem
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm

def products(request):
    context = {"items": Item.objects.all()}
    return render(request, "product-page.html", context)


class checkoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            "form": form,
            "object": order
        }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            print("The form is valid")
            return redirect('core:checkout')

class HomeView(ListView):
    model = Item
    paginate_by = 2
    template_name = "home.html"


class OrderSummaryView(LoginRequiredMixin, DetailView):
    def get(self, *args, **kwargs):
        try: 
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have and active order")
            return redirect("/")    
        context = {
            'object':order
        }
 
        return render(self.request,  "order_summary.html", context)



class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the ordered item is already in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity updated")

        else:
            messages.info(request, "Item added Successfully")
            order.items.add(order_item)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added Successfully")

    return redirect("core:order-summary")

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the ordered item is already in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "Item removed from your cart")
            return redirect("core:order-summary")

        else:
            messages.info(request, "This Item was not in your cart")
            return redirect("core:product", pk=pk)

    else:
        # add a message saying the user doesnt have an order
        messages.info(request, "You dont have an active order")
        return redirect("core:product", pk=pk)
    return redirect("core:product", pk=pk)



@login_required
def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the ordered item is already in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item, 
                user=request.user, 
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item's quantity updated")
            return redirect("core:order-summary")

        else:
            messages.info(request, "This Item was not in your cart")
            return redirect("core:order-summary")

    else:
        # add a message saying the user doesnt have an order
        messages.info(request, "You dont have an active order")
        return redirect("core:order-summary")
    return redirect("core:order-summary")
