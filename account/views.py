from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, CustomUserCreationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import Profile
#Nicolás Zapata Jurado
def signup(request):
    """
    Vista para el registro de nuevos usuarios con selección de rol.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            if user.is_staff:
                return redirect('property_panel')
            else:
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    """
    Vista para el inicio de sesión.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('account')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def account(request):
    """
    Vista del perfil del usuario, requiere estar logueado.
    """
    return render(request, 'account/account.html')

@login_required
def edit(request):
    """
    Vista para editar el perfil del usuario, manejando User y Profile.
    """
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('account')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'account/edit_profile.html', context)

def logout_view(request):
    """
    Vista para cerrar la sesión.
    """
    auth_logout(request)
    return redirect('home')