from django import forms
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    """
    Formulario para la edición del perfil del usuario.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
