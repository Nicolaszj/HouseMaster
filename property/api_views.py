from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from property.models import Property
from django.urls import reverse


@require_http_methods(["GET"])
def properties_api(request):
    """
    API REST que provee información de propiedades en formato JSON.
    
    Endpoint: /api/properties/
    
    Parámetros query opcionales:
    - type: 'Venta' o 'Arriendo'
    - status: 'Disponible', 'Vendida', 'Arrendada'
    - min_price: precio mínimo
    - max_price: precio máximo
    - limit: número máximo de resultados (default: 10)
    
    Retorna:
    {
        "count": int,
        "properties": [
            {
                "id": int,
                "title": str,
                "description": str,
                "type": str,
                "status": str,
                "price": float,
                "bedrooms": int,
                "bathrooms": int,
                "square_meters": float,
                "location": str,
                "address": str,
                "city": str,
                "department": str,
                "agent": {
                    "id": int,
                    "username": str,
                    "email": str
                },
                "url": str (enlace directo a la propiedad),
                "image_url": str (si tiene imagen)
            }
        ]
    }
    """
    # Filtros
    queryset = Property.objects.select_related('agent').all()
    
    property_type = request.GET.get('type')
    status = request.GET.get('status')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    limit = int(request.GET.get('limit', 10))
    
    if property_type:
        queryset = queryset.filter(type=property_type)
    
    if status:
        queryset = queryset.filter(status=status)
    
    if min_price:
        try:
            queryset = queryset.filter(price__gte=float(min_price))
        except ValueError:
            pass
    
    if max_price:
        try:
            queryset = queryset.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Limitar resultados
    queryset = queryset[:limit]
    
    # Construir respuesta JSON
    properties_data = []
    for prop in queryset:
        # URL absoluta de la propiedad
        property_url = request.build_absolute_uri(
            reverse('property_detail', args=[prop.id])
        )
        
        # URL de imagen si existe
        image_url = None
        if prop.image:
            image_url = request.build_absolute_uri(prop.image.url)
        
        property_dict = {
            'id': prop.id,
            'title': prop.title,
            'description': prop.description,
            'type': prop.type,
            'status': prop.status,
            'price': float(prop.price),
            'bedrooms': prop.bedrooms,
            'bathrooms': prop.bathrooms,
            'square_meters': float(prop.square_meters),
            'location': prop.location,
            'address': prop.address,
            'city': prop.city,
            'department': prop.department,
            'agent': {
                'id': prop.agent.id,
                'username': prop.agent.username,
                'email': prop.agent.email,
                'full_name': prop.agent.get_full_name() or prop.agent.username
            },
            'url': property_url,
            'image_url': image_url,
            'created_at': prop.created_at.isoformat() if hasattr(prop, 'created_at') else None,
        }
        properties_data.append(property_dict)
    
    response_data = {
        'count': len(properties_data),
        'properties': properties_data,
        'filters_applied': {
            'type': property_type,
            'status': status,
            'min_price': min_price,
            'max_price': max_price,
            'limit': limit
        }
    }
    
    return JsonResponse(response_data, json_dumps_params={'indent': 2})


@require_http_methods(["GET"])
def properties_for_sale_api(request):
    """
    API específica para propiedades en venta disponibles.
    
    Endpoint: /api/properties/for-sale/
    
    Parámetros opcionales:
    - limit: número máximo de resultados (default: 10)
    """
    limit = int(request.GET.get('limit', 10))
    
    properties = Property.objects.filter(
        type='Venta',
        status='Disponible'
    ).select_related('agent')[:limit]
    
    properties_data = []
    for prop in properties:
        property_url = request.build_absolute_uri(
            reverse('property_detail', args=[prop.id])
        )
        
        image_url = None
        if prop.image:
            image_url = request.build_absolute_uri(prop.image.url)
        
        properties_data.append({
            'id': prop.id,
            'title': prop.title,
            'price': float(prop.price),
            'bedrooms': prop.bedrooms,
            'bathrooms': prop.bathrooms,
            'square_meters': float(prop.square_meters),
            'location': prop.location,
            'url': property_url,
            'image_url': image_url,
        })
    
    return JsonResponse({
        'count': len(properties_data),
        'properties_for_sale': properties_data
    }, json_dumps_params={'indent': 2})


@require_http_methods(["GET"])
def api_documentation(request):
    """
    Documentación de la API en formato JSON
    
    Endpoint: /api/docs/
    """
    docs = {
        'api_name': 'HouseMaster Properties API',
        'version': '1.0',
        'description': 'API REST para consumir información de propiedades inmobiliarias',
        'base_url': request.build_absolute_uri('/api/'),
        'endpoints': [
            {
                'path': '/api/properties/',
                'method': 'GET',
                'description': 'Lista de todas las propiedades con filtros opcionales',
                'parameters': {
                    'type': 'Filtrar por tipo (Venta o Arriendo)',
                    'status': 'Filtrar por estado (Disponible, Vendida, Arrendada)',
                    'min_price': 'Precio mínimo',
                    'max_price': 'Precio máximo',
                    'limit': 'Número máximo de resultados (default: 10)'
                },
                'example': '/api/properties/?type=Venta&status=Disponible&limit=5'
            },
            {
                'path': '/api/properties/for-sale/',
                'method': 'GET',
                'description': 'Propiedades en venta disponibles',
                'parameters': {
                    'limit': 'Número máximo de resultados (default: 10)'
                },
                'example': '/api/properties/for-sale/?limit=5'
            },
            {
                'path': '/api/docs/',
                'method': 'GET',
                'description': 'Esta documentación'
            }
        ],
        'response_format': {
            'count': 'Número de propiedades retornadas',
            'properties': 'Array de objetos de propiedades',
            'property_fields': [
                'id', 'title', 'description', 'type', 'status',
                'price', 'bedrooms', 'bathrooms', 'square_meters',
                'location', 'address', 'city', 'department',
                'agent', 'url', 'image_url', 'created_at'
            ]
        },
        'cors': 'Enabled - Puede ser consumida desde cualquier origen',
        'authentication': 'No requiere autenticación',
        'rate_limit': 'Sin límite (ambiente de desarrollo)'
    }
    
    return JsonResponse(docs, json_dumps_params={'indent': 2})
