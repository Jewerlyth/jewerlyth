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


def aumentar_cantidad(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, id=item_id, user=request.user)
        item.cantidad += 1
        item.save()
    else:
        carrito = request.session.get('carrito', {})
        if item_id in carrito:
            carrito[item_id]['cantidad'] += 1
            request.session['carrito'] = carrito
    return redirect('ver_carrito')


def disminuir_cantidad(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, id=item_id, user=request.user)
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
        else:
            item.delete()
    else:
        carrito = request.session.get('carrito', {})
        if item_id in carrito:
            if carrito[item_id]['cantidad'] > 1:
                carrito[item_id]['cantidad'] -= 1
                request.session['carrito'] = carrito
            else:
                del carrito[item_id]
                request.session['carrito'] = carrito
    return redirect('ver_carrito')


#@login_required
def ver_carrito(request):
    if request.user.is_authenticated:
        carrito = Item.objects.filter(user=request.user)
    else:
        carrito = request.session.get('carrito', {}).values()

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
        if request.user.is_authenticated:
            carrito = Item.objects.filter(user=request.user)
        else:
            carrito_data = request.session.get('carrito', {})
            carrito = [
                {
                    'producto': Producto.objects.get(id=producto_id),
                    'cantidad': data['cantidad']
                }
                for producto_id, data in carrito_data.items()
            ]

        if not carrito:
            return redirect('ver_carrito')

        subtotal = sum(item['cantidad'] * item['producto'].precio for item in carrito)
        iva = subtotal * Decimal('0.16')  # 16% de IVA, ajusta según país
        envio = Decimal('100.00')  # Envío fijo, puedes hacerlo dinámico si gustas
        total = subtotal + iva + envio

        orden = Orden.objects.create(
            usuario=request.user if request.user.is_authenticated else None,  # Para no autentificados
            fecha=timezone.now(),
            subtotal=subtotal,
            iva=iva,
            envio=envio,
            total=total
        )

        for item in carrito:
            subtotal = item['producto'].precio * item['cantidad']  # Calcular subtotal
            DetalleOrden.objects.create(
                orden=orden,
                producto=item['producto'].titulo,
                precio_unitario=item['producto'].precio,
                cantidad=item['cantidad'],
                subtotal=subtotal  # Usar el cálculo aquí
            )

        if not request.user.is_authenticated:
            request.session['carrito'] = {}

        # Lógica del correo
        if request.POST.get('enviar_correo'):
            correo = request.POST.get('correo')
            if correo:
                enviar_recibo_email(orden, correo)
                messages.success(request, '¡Correo de recibo de compra enviado exitosamente!')  # Agregar el mensaje de éxito

        return render(request, 'Jewerlythwebapp/pago_exitoso.html', {'orden': orden})

    return render(request, 'Jewerlythwebapp/pago_simulado.html')




