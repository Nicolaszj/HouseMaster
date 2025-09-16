from django import forms
from .models import Compra

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['usuario', 'propiedad', 'nombre', 'telefono', 'direccion']
        # Nota: no incluimos 'fecha_compra' porque se genera automáticamente
