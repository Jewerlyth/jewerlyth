from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre=models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.nombre

class ProductoJewe(models.Model):
    titulo = models.CharField(max_length=50)
    categoria_prod = models.CharField(max_length=50, null=True, blank=True)
    imagen = models.ImageField(upload_to='productos', null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    categorias = models.ManyToManyField(Categoria)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'productojewe'
        verbose_name_plural = 'productosjewe'

    def __str__(self):
        return self.titulo
