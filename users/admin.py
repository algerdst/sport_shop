from django.contrib import admin

from .models import Basket, Order, User

admin.site.register(User)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['username', 'order_sum', 'order_quantity', 'delivery_address', 'order_date']
    filter_horizontal = ['products']


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    pass
