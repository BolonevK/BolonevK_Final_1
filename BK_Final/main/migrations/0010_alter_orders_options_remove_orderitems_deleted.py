# Generated by Django 4.0.6 on 2022-08-07 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_products_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orders',
            options={'ordering': ['id'], 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.RemoveField(
            model_name='orderitems',
            name='deleted',
        ),
    ]
