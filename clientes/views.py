from django.shortcuts import render, redirect
from .forms import FormularioRegistro, FormularioLogin
from .models import Cliente
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages


def clientes(request):
    registro_exitoso = False
    login_exitoso = False
    mensaje_login = None

    if request.method == 'POST':
        if 'nombres' in request.POST:  # Registro
            formulario_registro = FormularioRegistro(request.POST)
            formulario_login = FormularioLogin()
            if formulario_registro.is_valid():
                cliente = formulario_registro.save(commit=False)
                cliente.contrasena = make_password(formulario_registro.cleaned_data['contrasena'])
                cliente.save()
                registro_exitoso = True
        elif 'email' in request.POST and 'password' in request.POST:  # Login
            formulario_login = FormularioLogin(request.POST)
            formulario_registro = FormularioRegistro()
            if formulario_login.is_valid():
                email = formulario_login.cleaned_data['email']
                password = formulario_login.cleaned_data['password']
                try:
                    cliente = Cliente.objects.get(email=email)
                    if check_password(password, cliente.contrasena):
                        messages.success(request, f"Inicio de sesión exitoso. ¡Bienvenido {cliente.nombres}!")
                        return redirect('Home')

                    else:
                        mensaje_login = "Contraseña incorrecta"
                except Cliente.DoesNotExist:
                    mensaje_login = "Usuario no encontrado"
    else:
        formulario_registro = FormularioRegistro()
        formulario_login = FormularioLogin()

    return render(
        request,
        "clientes/clientes.html",
        {
            'miFormulario': formulario_registro,
            'miFormularioLogin': formulario_login,
            'registro_exitoso': registro_exitoso,
            'login_exitoso': login_exitoso,
            'mensaje_login': mensaje_login
        }
    )
from django.shortcuts import render

def home(request):
    # Aquí puedes renderizar la página de inicio
    return render(request, 'Jewerlythwebapp/home.html')

