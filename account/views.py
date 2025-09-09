from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm
from django.contrib.auth import login as auth_login, logout as auth_logout
#Nicolás Zapata Jurado
def signup(request):
    """
    Vista para el registro de nuevos usuarios.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('account')
    else:
        form = UserCreationForm()
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
    Vista para editar el perfil del usuario.
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'account/edit_profile.html', {'form': form})

def logout_view(request):
    """
    Vista para cerrar la sesión.
    """
    auth_logout(request)
    return redirect('home')