from django.shortcuts import render, get_object_or_404
from .models import Property

def home(request):
    """
    Vista para la página de inicio.
    
    Renderiza la plantilla home.html.
    """
    properties = Property.objects.all()
    return render(request, 'core/home.html', {'properties': properties})

def property_detail(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    gallery = list(prop.images.all())
    # Si no hay fotos en la galería, usamos la principal (image) si existe
    if not gallery and prop.image:
        # “fingimos” una galería de 1 con la image principal
        gallery = [{'image': prop.image, 'caption': 'Foto principal', 'is_cover': True}]
    context = {
        'prop': prop,
        'gallery': gallery,
    }
    return render(request, 'core/property_detail.html', context)