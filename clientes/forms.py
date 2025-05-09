# forms.py
from django import forms
from .models import Cliente

class FormularioRegistro(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombres', 'apellidos', 'email', 'contrasena']
        widgets = {
            'nombres': forms.TextInput(attrs={'style': 'width: 100%; height: 45px; font-size: 16px; padding: 5px;'}),
            'apellidos': forms.TextInput(attrs={'style': 'width: 100%; height: 45px; font-size: 16px; padding: 5px;'}),
            'email': forms.EmailInput(attrs={'style': 'width: 100%; height: 45px; font-size: 16px; padding: 5px;'}),
            'contrasena': forms.PasswordInput(attrs={'style': 'width: 300px; height: 45px; font-size: 16px; padding: 5px;'}),
        }



class FormularioLogin(forms.Form):
        email = forms.EmailField(
            label='Correo electrónico',
            required=True,
            widget=forms.EmailInput(attrs={'style': 'width: 300px; height: 45px; font-size: 16px; padding: 5px;'})
        )
        password = forms.CharField(
            label='Contraseña',
            required=True,
            widget=forms.PasswordInput(attrs={'style': 'width: 300px; height: 45px; font-size: 16px; padding: 5px;'})
        )
