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
            if hasattr(item, 'producto'):  # usuario autenticado
                cantidad = Decimal(item.cantidad)
                precio = Decimal(item.producto.precio)
            else:  # sesión (no autenticado)
                cantidad = Decimal(item.get('cantidad', 0))
                precio = Decimal(item.get('precio', 0))
            total += cantidad * precio
        except Exception as e:
            print(f"Error: {e}")
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
