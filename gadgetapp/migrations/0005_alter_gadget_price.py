# Generated by Django 5.0.3 on 2024-03-11 18:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gadgetapp", "0004_cart_cartitems"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gadget",
            name="price",
            field=models.IntegerField(),
        ),
    ]
