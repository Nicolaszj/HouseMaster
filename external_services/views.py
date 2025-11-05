from django.shortcuts import render
from django.contrib import messages
from .services import ExternalServiceFactory


def partner_products(request):
    """
    Vista: /productos-aliados
    
    Consume el servicio del equipo precedente y muestra
    sus productos/propiedades en nuestra aplicación.
    """
    # Crear servicio usando el factory
    partner_service = ExternalServiceFactory.create_partner_service()
    
    # Verificar disponibilidad
    service_available = partner_service.is_available()
    
    # Obtener datos
    result = partner_service.fetch_data()
    
    if not result.get('success'):
        messages.warning(
            request,
            f"No se pudo conectar con el servicio aliado: {result.get('message', 'Error desconocido')}"
        )
    
    context = {
        'service_available': service_available,
        'result': result,
        'products': result.get('data', []),
        'count': result.get('count', 0),
    }
    
    return render(request, 'external_services/partner_products.html', context)


def weather_widget(request):
    """
    Vista: /clima
    
    Consume API del clima de OpenWeatherMap.
    Puede ser incluida como widget en otras páginas.
    """
    city = request.GET.get('city', 'Bogota')
    
    # Crear servicio del clima
    weather_service = ExternalServiceFactory.create_weather_service(city=city)
    
    # Obtener datos del clima
    weather_data = weather_service.fetch_data()
    
    context = {
        'weather': weather_data,
        'city': city,
    }
    
    return render(request, 'external_services/weather_widget.html', context)
