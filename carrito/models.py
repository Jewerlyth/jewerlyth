from django.db import models
from productos.models import ProductoJewe
from django.contrib.auth.models import User
from decimal import Decimal

class Item(models.Model):
    producto = models.ForeignKey(ProductoJewe, on_delete=models.CASCADE)  # Producto añadido al carrito
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relacionamos el carrito con un usuario
    cantidad = models.PositiveIntegerField(default=1)  # Cantidad del producto
    added = models.DateTimeField(auto_now_add=True)  # Fecha en que se añadió el producto

    def __str__(self):
        return f"{self.producto.titulo} x {self.cantidad}"

class Orden(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Usuario asociado
    fecha = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    envio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        if self.usuario:
            return f"Orden #{self.id} - {self.usuario.username}"
        return f"Orden #{self.id} - Usuario anónimo"


class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, related_name='detalles', on_delete=models.CASCADE)
    producto = models.CharField(max_length=200)
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    envio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.producto} x {self.cantidad} (Orden #{self.orden.id})"

    def calcular_subtotal(self):
        return Decimal(self.precio_unitario) * self.cantidad