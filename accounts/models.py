from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
class Staff(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100, default='Executive', choices=(
        ('Store Keeper', 'Store Keeper'), ('Executive', 'Executive'), ('Sales officer', 'Sales officer'),
        ('Marketing officer', 'Marketing officer'),))
    birth_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user_id.username


class Customer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_badge = models.CharField(max_length=50,
                                  choices=(('Gold', 'Gold'), ('Platinum', 'Platinum'), ('Bronze', 'Bronze')))
    contact_number = models.CharField(max_length=15)
    is_user_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user_id.username


class CustomerAddress(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
