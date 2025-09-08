from django.shortcuts import render
from .models import Property

def home(request):
    """
    Vista para la página de inicio.
    
    Renderiza la plantilla home.html.
    """
    properties = Property.objects.all()
    return render(request, 'core/home.html', {'properties': properties})
