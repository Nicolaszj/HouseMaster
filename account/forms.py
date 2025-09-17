from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    """
    Formulario para la edición del perfil del usuario (datos del User).
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    """
    Formulario para la edición del perfil del usuario (datos del Profile).
    """
    class Meta:
        model = Profile
        fields = ['phone_number']

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('', 'Selecciona un tipo de cuenta'), 
        ('cliente', 'Registrarme como Cliente'),
        ('agente', 'Registrarme como Agente'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Tipo de cuenta")

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.attrs.update({'class': 'form-select'})
        for field_name in ['first_name', 'last_name', 'email']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['role'] == 'agente':
            user.is_staff = True
        if commit:
            user.save()
        return user