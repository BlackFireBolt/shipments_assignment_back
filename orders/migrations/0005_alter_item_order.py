# Generated by Django 4.1 on 2022-09-30 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_item_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="order",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="orders.order",
            ),
        ),
    ]
