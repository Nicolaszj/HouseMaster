from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import json
import os


import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings

openai.api_key = os.getenv("OPENAI_API_KEY")

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


def chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente inmobiliario útil."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=200
            )
            answer = response['choices'][0]['message']['content']
            return JsonResponse({"reply": answer})
        except Exception as e:
            return JsonResponse({"reply": "Error al procesar tu solicitud."})
    return JsonResponse({"reply": "Método no permitido."}, status=405)