"""
Solución temporal: Middleware de traducción manual sin archivos .mo
Funciona sin necesidad de compilar gettext
"""

class SimpleTranslationMiddleware:
    """Middleware simple para traducir sin archivos .mo"""
    
    TRANSLATIONS = {
        'en': {
            'Inicio': 'Home',
            'Propiedades': 'Properties',
            'Contacto': 'Contact',
            'Mis Propiedades': 'My Properties',
            'Gestionar Compras': 'Manage Purchases',
            'Favoritos': 'Favorites',
            'Visitas': 'Visits',
            'Compras': 'Purchases',
            'Perfil': 'Profile',
            'Cerrar Sesión': 'Logout',
            'Iniciar Sesión': 'Login',
            'Registrarse': 'Sign Up',
            'Chat': 'Chat',
            'Venta': 'Sale',
            'Arriendo': 'Rent',
            'Disponible': 'Available',
            'Vendida': 'Sold',
            'Arrendada': 'Rented',
            'Habitaciones': 'Bedrooms',
            'Baños': 'Bathrooms',
            'Metros Cuadrados': 'Square Meters',
            'Precio': 'Price',
            'Ver Detalles': 'View Details',
            'Contactar Agente': 'Contact Agent',
            'Agregar a Favoritos': 'Add to Favorites',
            'Eliminar de Favoritos': 'Remove from Favorites',
            'Agendar Visita': 'Schedule Visit',
            'Comprar': 'Buy',
            'Real Estate': 'Real Estate',
        }
    }
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Obtener el idioma actual
        from django.utils import translation
        current_lang = translation.get_language()
        
        # Activar el idioma
        if current_lang:
            translation.activate(current_lang)
        
        response = self.get_response(request)
        return response
