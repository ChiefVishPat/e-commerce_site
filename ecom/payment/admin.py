from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

#register model on admin site
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

#create an OrderItem inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


#extend order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderItemInline]


admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)