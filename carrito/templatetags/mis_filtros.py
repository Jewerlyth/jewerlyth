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
    return next((item for item in carrito if getattr(item, 'producto', {}).id == producto_id), None)

@register.filter
def calc_subtotal(carrito):
    total = Decimal(0)
    for item in carrito:
        try:
            cantidad = item.cantidad if hasattr(item, 'cantidad') else item.get('cantidad', 0)
            precio = item.producto.precio if hasattr(item, 'producto') else item.get('precio', 0)
            total += Decimal(cantidad) * Decimal(precio)
        except Exception:
            continue
    return total

@register.filter
def calc_iva(carrito):
    subtotal = calc_subtotal(carrito)
    return round(subtotal * Decimal(0.16), 2)

@register.filter
def calc_envio(carrito):
    return Decimal(100.00)

@register.filter
def calc_total(carrito):
    subtotal = calc_subtotal(carrito)
    iva = subtotal * Decimal(0.16)
    envio = Decimal(100.00)
    return round(subtotal + iva + envio, 2)
