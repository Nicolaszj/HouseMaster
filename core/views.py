from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.http import JsonResponse
from propiedades.models import Propiedad
from propiedades.forms import CompraForm
import json, openai


# Páginas generales
def home(request): return render(request, 'home.html')
def contacto(request): return render(request, "core/contacto.html")
def perfil(request): return render(request, 'perfil.html')


# Chatbot-Santiago
def chatbot_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')
        response = openai.ChatCompletion.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": message}]
        )
        return JsonResponse({'reply': response.choices[0].message.content})
    return JsonResponse({'reply': 'Hola, soy tu chatbot!'})


# Autenticación
def signup(request): return render(request, 'signup.html')
def login_view(request): return render(request, 'login.html')
def logout_view(request): logout(request); return redirect('home')


# Propiedades y compras
def propiedades(request):
    return render(request, 'core/propiedades.html', {'propiedades': Propiedad.objects.filter(disponible=True)})

def propiedad_detalle(request, propiedad_id):
    return render(request, 'core/propiedad_detalle.html', {'propiedad': get_object_or_404(Propiedad, id=propiedad_id)})

def comprar_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)
    form = CompraForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        compra = form.save(commit=False)
        compra.propiedad = propiedad
        compra.save()
        return redirect('propiedades')
    return render(request, 'core/comprar_propiedad.html', {'form': form, 'propiedad': propiedad})
