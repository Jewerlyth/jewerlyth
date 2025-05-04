from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ProductoJewe, Item,  Orden, DetalleOrden
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse
from decimal import Decimal
from django.contrib import messages

#def agregar_al_carrito(request, producto_id):
 #   producto = get_object_or_404(ProductoJewe, id=producto_id)
  #  item, creado = Item.objects.get_or_create(user=request.user, producto=producto)
  #  print("Agregado por:", request.user)

  #  if not creado:
   #     item.cantidad += 1
   #     item.save()
   # return redirect('ver_carrito')

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(ProductoJewe, id=producto_id)

    # Si el usuario está autenticado, se guarda en la base de datos
    if request.user.is_authenticated:
        item, creado = Item.objects.get_or_create(user=request.user, producto=producto)
        print("Agregado por:", request.user)

        if not creado:
            item.cantidad += 1
            item.save()
    else:
        # Si el usuario no está autenticado, se guarda el producto en la sesión
        carrito = request.session.get('carrito', [])

        # Verificamos si el producto ya está en el carrito
        producto_en_carrito = next((item for item in carrito if item['producto_id'] == producto.id), None)

        if producto_en_carrito:
            # Si el producto ya está en el carrito, incrementamos la cantidad
            producto_en_carrito['cantidad'] += 1
        else:
            # Si no está, lo agregamos al carrito
            carrito.append({'producto_id': producto.id, 'cantidad': 1})

        # Guardamos el carrito actualizado en la sesión
        request.session['carrito'] = carrito

    return redirect('ver_carrito')


def aumentar_cantidad(request, producto_id):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, user=request.user, producto_id=producto_id)
        item.cantidad += 1
        item.save()
    else:
        carrito = request.session.get('carrito', [])
        for item in carrito:
            if item['producto_id'] == producto_id:
                item['cantidad'] += 1
                break
        request.session['carrito'] = carrito
    return redirect('ver_carrito')



def disminuir_cantidad(request, producto_id):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, user=request.user, producto_id=producto_id)
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
        else:
            item.delete()
    else:
        carrito = request.session.get('carrito', [])
        for i, item in enumerate(carrito):
            if item['producto_id'] == producto_id:
                if item['cantidad'] > 1:
                    item['cantidad'] -= 1
                else:
                    carrito.pop(i)
                break
        request.session['carrito'] = carrito
    return redirect('ver_carrito')


#@login_required
def ver_carrito(request):
    if request.user.is_authenticated:
        carrito = Item.objects.filter(user=request.user)
    else:
        carrito_sesion = request.session.get('carrito', [])
        carrito = []
        for item in carrito_sesion:
            producto = get_object_or_404(ProductoJewe, id=item['producto_id'])
            carrito.append({
                'producto': producto,
                'cantidad': item['cantidad'],
                'precio': str(producto.precio)  # str() si es Decimal
            })
    return render(request, 'Jewerlythwebapp/carrito.html', {'carrito': carrito})



def enviar_recibo_email(orden, correo):
    asunto = f"Recibo de tu compra - Orden #{orden.id}"
    destinatario = [correo]

    cuerpo = render_to_string('Jewerlythwebapp/correo_recibo.html', {
        'orden': orden,
        'usuario': orden.usuario,  # Solo si deseas usar {{ usuario.username }}
    })

    email = EmailMessage(asunto, cuerpo, to=destinatario)
    email.content_subtype = 'html'  # Para que se renderice el HTML
    email.send()

def recibir_correo(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        orden_id = request.POST.get('orden_id')

        if correo and orden_id:
            orden = Orden.objects.get(id=orden_id)
            enviar_recibo_email(orden, correo)
            return HttpResponse("Recibo enviado al correo proporcionado.")
        else:
            return HttpResponse("Faltan datos necesarios.", status=400)

    return redirect('ver_carrito')

#@login_required
def pago_simulado(request):
    # Esta vista solo muestra el formulario de simulación de pago
    return render(request, 'Jewerlythwebapp/pago_simulado.html')


def pago_exitoso(request):
    if request.method == 'POST':
        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            carrito = Item.objects.filter(user=request.user)
        else:
            # Asegurarse de que sea una lista
            carrito_data = request.session.get('carrito', [])
            if not isinstance(carrito_data, list):
                carrito_data = []  # Evita errores si fue mal seteado
            carrito = [
                {
                    'producto': ProductoJewe.objects.get(id=item['producto_id']),
                    'cantidad': item['cantidad']
                }
                for item in carrito_data
            ]

        # Si no hay productos en el carrito, redirigir al carrito
        if not carrito:
            return redirect('ver_carrito')

        # Calcular subtotal, IVA, envío y total
        subtotal = sum(item['cantidad'] * item['producto'].precio for item in carrito)
        iva = subtotal * Decimal('0.16')  # 16% de IVA
        envio = Decimal('100.00')  # Envío fijo
        total = subtotal + iva + envio

        # Crear la orden, asignando el usuario solo si está autenticado
        orden = Orden.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            fecha=timezone.now(),
            subtotal=subtotal,
            iva=iva,
            envio=envio,
            total=total
        )

        # Crear los detalles de la orden
        for item in carrito:
            subtotal_item = item['producto'].precio * item['cantidad']
            DetalleOrden.objects.create(
                orden=orden,
                producto=item['producto'].titulo,
                precio_unitario=item['producto'].precio,
                cantidad=item['cantidad'],
                subtotal=subtotal_item
            )

        # Limpiar el carrito de la sesión correctamente
        if not request.user.is_authenticated:
            request.session['carrito'] = []  # ✅ Limpiar con lista, no dict

        # Lógica para enviar el recibo por correo
        if request.POST.get('enviar_correo'):
            correo = request.POST.get('correo')
            if correo:
                enviar_recibo_email(orden, correo)
                messages.success(request, '¡Correo de recibo de compra enviado exitosamente!')

        # Mostrar la página de pago exitoso
        return render(request, 'Jewerlythwebapp/pago_exitoso.html', {'orden': orden})

    # Si no es un POST, mostrar una página simulada
    return render(request, 'Jewerlythwebapp/pago_simulado.html')
