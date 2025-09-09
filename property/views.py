from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Property
# Create your views here.
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
    return render(request, 'property_detail.html', context)