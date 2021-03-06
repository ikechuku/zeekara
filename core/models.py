from django.db import models
from django.conf import settings
from django.shortcuts import reverse


CATERGORY_CHOICES = (("S", "Shirt"), ("SW", "Sport Wear"), ("OW", "Outwear"))

LABEL_CHOICES = (("P", "primary"), ("S", "secondary"), ("F", "danger"))


class Item(models.Model):
    title = models.CharField(max_length=50)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATERGORY_CHOICES, max_length=50, default="S")
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, default="P")
    description = models.TextField(
        default="Lorem ipsum dolor sit amet consectetur adipisicing elit. Quidem id asperiores soluta aut sunt, recusandae sit iusto?"
    )

    def __str__(self):
        return self.title

    def get_percentage_saved(self):
        saved = self.price - self.discount_price
        percentage_saved = round(saved/self.price * 100)
        return percentage_saved

    def  get_absolute_url(self):
        return reverse("core:product", kwargs={"pk": self.pk})

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={"pk": self.pk})

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={"pk": self.pk})


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_price(self):
        return round(self.quantity * self.item.price, 2)
    
    def get_total_discount_price(self):
        return round(self.quantity * self.item.discount_price, 2)
        
    def get_amount_saved(self):
        saved = round(self.get_total_price() - self.get_total_discount_price())
        return saved
    
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        return round(self.get_total_price())
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return round(total, 2)
    
    def count(self):
        return self.items.count()