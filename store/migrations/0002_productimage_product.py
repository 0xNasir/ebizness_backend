# Generated by Django 4.2 on 2023-04-08 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(default='2', on_delete=django.db.models.deletion.CASCADE, to='store.product'),
            preserve_default=False,
        ),
    ]
