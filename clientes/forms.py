from django import forms

class FormularioRegistro(forms.Form):
    nombres = forms.CharField(
        label='Nombre(s)',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'style': 'width: 100%; height: 45px; font-size: 16px; padding: 5px;'})
    )
    apellidos = forms.CharField(
        label='Apellidos',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'style': 'width: 100%; height: 45px; font-size: 16px; padding: 5px;'})
    )
    email = forms.EmailField(
        label='Correo electrónico',
        required=True,
        widget=forms.EmailInput(attrs={'style': 'width: 100%; height: 45px; font-size: 16px; padding: 5px;'})
    )
    contrasena = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(attrs={'style': 'width: 300px; height: 45px; font-size: 16px; padding: 5px;'})
    )



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
