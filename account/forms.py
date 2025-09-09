from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class SignUpForm(UserCreationForm):
    """
    Formulario de registro personalizado que incluye el rol y el teléfono.
    """
    # Excluimos el rol de Administrador de las opciones de registro público
    USER_ROLE_CHOICES = [
        (role, label) for role, label in Profile.Role.choices if role != Profile.Role.ADMIN
    ]
    
    role = forms.ChoiceField(choices=USER_ROLE_CHOICES, required=True, label="Soy")
    telefono = forms.CharField(max_length=20, required=False, help_text='Opcional (necesario para Agentes).')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Guardamos los datos extra en el perfil del usuario que se crea automáticamente
            profile = user.profile
            profile.role = self.cleaned_data['role']
            profile.telefono = self.cleaned_data['telefono']
            profile.save()
        return user

class UserUpdateForm(forms.ModelForm):
    """
    Formulario para editar los datos básicos del usuario (modelo User).
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    """
    Formulario para editar los datos del perfil (modelo Profile), como el teléfono.
    """
    class Meta:
        model = Profile
        fields = ['telefono']

