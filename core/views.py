from django.shortcuts import render
from property.services.property_service import PropertyService


def home(request):
    """
    Vista para la página de inicio.
    
    Utiliza el Service Layer para acceder a las propiedades.
    DIP: Depende del servicio, no directamente del modelo.
    """
    # Usar el servicio en lugar de acceder directamente al modelo
    service = PropertyService()
    properties = service.get_available_properties()[:6]  # Mostrar solo 6 en home
    
    return render(request, 'core/home.html', {'properties': properties})