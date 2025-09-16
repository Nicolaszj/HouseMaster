from django.shortcuts import render, get_object_or_404, redirect
from .models import Propiedad
from .forms import CompraForm  # si tienes un formulario CompraForm

# LISTA DE TODAS LAS PROPIEDADES
def propiedades(request):
    propiedades = Propiedad.objects.filter(disponible=True)
    return render(request, 'propiedades/propiedades.html', {'propiedades': propiedades})

# DETALLE DE UNA PROPIEDAD
def propiedad_detalle(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)
    return render(request, 'propiedades/propiedad_detalle.html', {'propiedad': propiedad})


