from django.shortcuts import render, get_object_or_404, redirect
from propiedades.models import Propiedad
from .forms import CompraForm  # si tienes un formulario de compra

def comprar_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.propiedad = propiedad  # <- aquí
            compra.save()
            propiedad.disponible = False
            propiedad.save()
            return redirect('propiedades')
    else:
        form = CompraForm()
    return render(request, 'compras/comprar_propiedad.html', {'propiedad': propiedad, 'form': form})
