from django import forms
from .models import MensajeSoporte

class SoporteForm(forms.ModelForm):
    class Meta:
        model = MensajeSoporte
        fields = ['nombre', 'correo', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
