# Generated by Django 4.0.4 on 2022-07-04 18:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_order_items_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='added',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 7, 4, 21, 35, 2, 902713)),
            preserve_default=False,
        ),
    ]