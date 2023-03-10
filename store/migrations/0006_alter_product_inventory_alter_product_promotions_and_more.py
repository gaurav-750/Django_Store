# Generated by Django 4.1.6 on 2023-02-03 13:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='inventory',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='promotions',
            field=models.ManyToManyField(blank=True, to='store.promotion'),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
