from django.shortcuts import render, HttpResponse, redirect
from .forms import SoporteForm
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


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

def get_response(user_input):
    user_input = user_input.lower()

    if "hola" in user_input:
        return "Buenos días, soy el bot de la joyería JEWERLYTH. ¿En qué le puedo ayudar?"

    elif "joyeria" in user_input or "joya" in user_input:
        return "Tenemos anillos, cadenas y aretes en oro y plata."

    elif "precio" in user_input:
        return "Los precios varían desde 100 a 300 pesos según el tipo de joya."

    elif "horario" in user_input or "abren" in user_input:
        return "Estamos disponibles de lunes a sábado de 9:00 a.m. a 4:00 p.m."

    elif "gracias" in user_input or "gracias!" in user_input:
        return "¡Con gusto! ¿Necesitas algo más?"

    elif user_input.strip() == "":
        return "Por favor, selecciona una opción para poder ayudarte."

    elif "envío" in user_input or "envios" in user_input:
        return "Ofrecemos envío estándar (3-5 días) y envío exprés (1-2 días). Todos los envíos se realizan por paquetería segura."

    elif "ayuda" in user_input or "correos" in user_input:
        return "Si necesitas ayuda, puedes escribirnos a joyeria@jewerlyth.com o contactarnos por WhatsApp al xxx-xxx-xxxx."

    else:
        return "Lo siento, no entendí bien. ¿Podrías reformular la pregunta?"

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_text = data.get("message", "")
        response = get_response(user_text)
        return JsonResponse({"response": response})
def home(request):
    return render(request, 'Jewerlythwebapp/home.html')