from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return Decimal(value) * Decimal(arg)
    except (ValueError, TypeError):
        return Decimal(0)

@register.filter
def get_item(carrito, producto_id):
    return next((item for item in carrito if item.producto.id == producto_id), None)

@register.filter
def calc_subtotal(carrito):
    return sum(Decimal(item.cantidad) * Decimal(item.producto.precio) for item in carrito)

@register.filter
def calc_iva(carrito):
    subtotal = sum(Decimal(item.cantidad) * Decimal(item.producto.precio) for item in carrito)
    return round(subtotal * Decimal(0.16), 2)

@register.filter
def calc_envio(carrito):
    return Decimal(100.00)  # Por ejemplo, un costo fijo

@register.filter
def calc_total(carrito):
    subtotal = sum(Decimal(item.cantidad) * Decimal(item.producto.precio) for item in carrito)
    iva = subtotal * Decimal(0.16)
    envio = Decimal(100.00)  # O puedes hacer dinámico si lo deseas
    return round(subtotal + iva + envio, 2)
