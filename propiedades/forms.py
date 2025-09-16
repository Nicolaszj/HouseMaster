from django import forms
from .models import Compra

class CompraForm(forms.ModelForm):
    nombre = forms.CharField(max_length=100, required=True, label="Tu nombre")
    telefono = forms.CharField(max_length=20, required=True, label="Teléfono")
    direccion = forms.CharField(max_length=200, required=True, label="Dirección")

    class Meta:
        model = Compra
        fields = ["nombre", "telefono", "direccion"]  # 7