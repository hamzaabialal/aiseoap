# Generated by Django 5.0.6 on 2024-06-29 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopifyproducts', '0006_products_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_url',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
