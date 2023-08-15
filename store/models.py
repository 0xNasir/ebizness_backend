from django.db import models

from accounts.models import Staff, Customer


# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='brand')
    description = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text='In KG')
    dimension = models.CharField(max_length=50, help_text='h*w*l in cm', blank=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price2 = models.DecimalField(max_digits=10, decimal_places=2)
    added_on = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(Staff, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE)

    def __str__(self):
        return self.image.url


class Favourite(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    fav_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.customer.user_id.get_username()


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.customer.user_id.get_username()
