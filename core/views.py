import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.http import JsonResponse
import openai

from propiedades.models import Propiedad
from propiedades.forms import CompraForm



# Página principal
def home(request):
    return render(request, 'home.html')

# Propiedades

# Contacto
def contacto(request):
    return render(request, 'contacto.html')

# Perfil
def perfil(request):
    return render(request, 'perfil.html')

import json
from django.http import JsonResponse
import openai

def chatbot_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')

        # Llamada a OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": message}]
        )

        reply = response.choices[0].message.content

        return JsonResponse({'reply': reply})

    return JsonResponse({'reply': 'Hola, soy tu chatbot!'})


# Autenticación
def signup(request):
    return render(request, 'signup.html')

def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')


# LISTA DE TODAS LAS PROPIEDADES
def propiedades(request):
    propiedades = Propiedad.objects.filter(disponible=True)
    return render(request, 'core/propiedades.html', {'propiedades': propiedades})



# DETALLE DE UNA PROPIEDAD
def propiedad_detalle(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)
    return render(request, 'core/propiedad_detalle.html', {'propiedad': propiedad})

# Comprar una propiedad
def comprar_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.propiedad = propiedad
            compra.save()
            return redirect('propiedades')  # o a 'propiedad_detalle' si quieres mostrar la comprada
    else:
        form = CompraForm()
    return render(request, 'core/comprar_propiedad.html', {'form': form, 'propiedad': propiedad})

def contacto(request):
    return render(request, 'core/contacto.html')
