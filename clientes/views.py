from django.shortcuts import render
from .forms import FormularioRegistro, FormularioLogin

def clientes(request):
    formulario_registro = FormularioRegistro()
    formulario_login = FormularioLogin()
    return render(
        request,
        "clientes/clientes.html",
        {
            'miFormulario': formulario_registro,
            'miFormularioLogin': formulario_login
        }
    )
# Create your views here.
