from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import Propiedad


# PERFIL (requiere login)
@login_required
def perfil(request):
    return render(request, 'core/perfil.html')


# REGISTRO
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})


# LOGIN
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('home')


# PÁGINA DE INICIO
def home(request):
    propiedades = Propiedad.objects.all()[:3]  # solo 3 destacadas
    return render(request, 'core/home.html', {'propiedades': propiedades})


# LISTA DE TODAS LAS PROPIEDADES
def propiedades(request):
    propiedades = Propiedad.objects.all()
    return render(request, 'core/propiedades.html', {'propiedades': propiedades})


# DETALLE DE UNA PROPIEDAD
def propiedad_detalle(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)
    return render(request, 'core/propiedad_detalle.html', {'propiedad': propiedad})


# PÁGINA DE CONTACTO
def contacto(request):
    return render(request, 'core/contacto.html')
