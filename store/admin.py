from django.contrib import admin

from store.models import Category, Brand, Product, ProductImage, Favourite, Cart

# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Favourite)
admin.site.register(Cart)
