from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

#register model on admin site
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
