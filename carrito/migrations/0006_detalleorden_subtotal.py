# Generated by Django 5.2 on 2025-05-03 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0005_detalleorden_envio_detalleorden_iva_orden_envio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleorden',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
