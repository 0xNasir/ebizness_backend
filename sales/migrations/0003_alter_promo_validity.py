# Generated by Django 4.2 on 2023-07-01 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_alter_payment_payment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promo',
            name='validity',
            field=models.DateField(blank=True),
        ),
    ]
