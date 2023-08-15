from django.contrib import admin

from sales.models import Promo, Order, Payment, OrderProduct

# Register your models here.
admin.site.register(Promo)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(OrderProduct)
