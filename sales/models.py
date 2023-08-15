from django.db import models

from accounts.models import Customer, CustomerAddress, Staff
from store.models import Product


# Create your models here.
class Promo(models.Model):
    promo_code = models.CharField(max_length=10)
    promo_type = models.CharField(max_length=20,
                                  choices=(('Percentage', 'Percentage'), ('Fixed Amount', 'Fixed Amount')))
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Minimum order amount')
    description = models.TextField()
    started_at = models.DateField()
    validity = models.DateField(blank=True)
    invoke = models.BooleanField(default=False)

    def __str__(self):
        return self.promo_code


class Payment(models.Model):
    payment_type = models.CharField(max_length=200, choices=(
        ('Direct Bank Transfer', 'Direct Bank Transfer'), ('Pay on delivery', 'Pay on delivery'),
        ('Pay on cash', 'Pay on cash')))
    payment_status = models.CharField(max_length=100, choices=(('Not paid', 'Not paid'), ('Paid', 'Paid')))
    paid_id = models.CharField(max_length=100)
    payment_received_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.paid_id


class Order(models.Model):
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    net_price = models.DecimalField(max_digits=10, decimal_places=2)
    promo_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    is_promo_applied = models.BooleanField(default=False)
    promo = models.ForeignKey(Promo, on_delete=models.CASCADE)
    delivery_location = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=100, choices=(
        ('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Declined', 'Declined'), ('Cancelled', 'Cancelled'),
        ('Processing', 'Processing'), ('Packaging', 'Packaging'), ('Shifted to Rider', 'Shifted to Rider'),
        ('Delivered', 'Delivered')))
    order_processed_by = models.ForeignKey(Staff, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class OrderProduct(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.order_id.id)
