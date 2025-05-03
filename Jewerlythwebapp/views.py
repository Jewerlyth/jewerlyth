from django.shortcuts import render, HttpResponse, redirect
from .forms import SoporteForm
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    return render(request, "Jewerlythwebapp/home.html")


def carrito(request):
    return render(request, "Jewerlythwebapp/carrito.html")


def soporte(request):
    if request.method == 'POST':
        form = SoporteForm(request.POST)
        if form.is_valid():
            form.save()
            # Enviar el correo
            send_mail(
                'Nuevo mensaje de soporte',  # Asunto del correo
                f'Nombre: {form.cleaned_data["nombre"]}\nCorreo: {form.cleaned_data["correo"]}\nMensaje: {form.cleaned_data["mensaje"]}',  # Cuerpo del correo
                settings.EMAIL_HOST_USER,  # Correo que envía
                ['jewerlyth@gmail.com'],  # Correo al que se envía (correo de soporte)
                fail_silently=False,
            )
            return render(request, 'Jewerlythwebapp/soporte.html', {'form': SoporteForm(), 'enviado': True})
    else:
        form = SoporteForm()
    return render(request, 'Jewerlythwebapp/soporte.html', {'form': form})
