# Generated by Django 4.2 on 2023-08-10 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_promo_min_order_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
    ]
