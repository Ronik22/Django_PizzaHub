# Generated by Django 3.1.6 on 2021-05-01 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0007_contact'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name_plural': 'Contact Us Entries'},
        ),
    ]
