# Generated by Django 4.2.3 on 2023-07-19 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cake_app', '0002_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_active',
            field=models.BooleanField(blank=True, null=True, verbose_name='Статус заказа'),
        ),
    ]
