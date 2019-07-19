from django.contrib import admin
from . import models as mod

admin.site.register(mod.Item)
admin.site.register(mod.OrderItem)
admin.site.register(mod.Order)
