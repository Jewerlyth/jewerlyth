# Generated by Django 5.2 on 2025-05-02 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_producto_precio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='contenido',
            new_name='categoria',
        ),
    ]
