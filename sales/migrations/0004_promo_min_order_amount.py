# Generated by Django 4.2 on 2023-08-10 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_alter_promo_validity'),
    ]

    operations = [
        migrations.AddField(
            model_name='promo',
            name='min_order_amount',
            field=models.DecimalField(decimal_places=2, default=1, help_text='Minimum order amount', max_digits=10),
            preserve_default=False,
        ),
    ]
