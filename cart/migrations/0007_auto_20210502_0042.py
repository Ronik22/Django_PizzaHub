# Generated by Django 3.1.6 on 2021-05-01 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_auto_20210502_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='Unknown', max_length=200),
        ),
    ]
