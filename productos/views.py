from django.shortcuts import render
from productos.models import Categoria, ProductoJewe
from carrito.models import Item  # importa el modelo

# Create your views here.

def productos(request):
    productosjewe = ProductoJewe.objects.all()
    categorias = Categoria.objects.all()
    if request.user.is_authenticated:
        carrito = Item.objects.filter(user=request.user)
    else:
        carrito = Item.objects.none()  # Si el usuario no está autenticado, no hay carrito

    return render(request, "productos/productos.html", {
        "productosjewe": productosjewe,
        "categorias": categorias
    })


def categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    productosjewe = ProductoJewe.objects.filter(categorias=categoria)
    return render(request, "productos/categorias.html", {
        'categoria': categoria,  # <- nombre corregido
        "productosjewe": productosjewe
    })
