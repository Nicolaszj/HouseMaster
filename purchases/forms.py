from django import forms
from .models import Purchase
from decimal import Decimal


class PurchaseForm(forms.ModelForm):
    """Formulario para crear una compra de propiedad"""
    
    class Meta:
        model = Purchase
        fields = ['payment_method', 'down_payment', 'notes']
        widgets = {
            'payment_method': forms.Select(attrs={
                'class': 'form-control',
            }),
            'down_payment': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la cuota inicial',
                'min': '0',
                'step': '0.01',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Notas adicionales (opcional)',
            }),
        }
        labels = {
            'payment_method': 'Método de Pago',
            'down_payment': 'Cuota Inicial',
            'notes': 'Notas Adicionales',
        }
    
    def __init__(self, *args, **kwargs):
        self.property = kwargs.pop('property', None)
        super().__init__(*args, **kwargs)
        
        # Hacer notes opcional visualmente
        self.fields['notes'].required = False
        
        # Establecer valor inicial de down_payment si hay propiedad
        if self.property:
            # Sugerir 20% como cuota inicial
            suggested_down_payment = (self.property.price * Decimal('0.20')).quantize(Decimal('0.01'))
            self.fields['down_payment'].widget.attrs['placeholder'] = f'Sugerido: ${suggested_down_payment:,.2f} (20%)'
    
    def clean_down_payment(self):
        """Valida que la cuota inicial sea razonable"""
        down_payment = self.cleaned_data.get('down_payment')
        
        if down_payment and down_payment < 0:
            raise forms.ValidationError("La cuota inicial no puede ser negativa")
        
        if self.property and down_payment:
            if down_payment > self.property.price:
                raise forms.ValidationError("La cuota inicial no puede ser mayor al precio de la propiedad")
        
        return down_payment


class PurchaseAdminForm(forms.ModelForm):
    """Formulario para administrar compras (staff/admin)"""
    
    class Meta:
        model = Purchase
        fields = ['status', 'payment_confirmation', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'payment_confirmation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código de confirmación',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
        }
