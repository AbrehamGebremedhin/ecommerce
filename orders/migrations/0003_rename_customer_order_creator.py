# Generated by Django 4.2.6 on 2023-11-03 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='customer',
            new_name='creator',
        ),
    ]