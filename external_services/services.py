"""
Servicio para consumir APIs externas.
Implementa DIP (Dependency Inversion Principle) con una interfaz base.
"""
import requests
from abc import ABC, abstractmethod
from typing import Dict, List, Any


class ExternalServiceInterface(ABC):
    """
    Interfaz base para servicios externos.
    Implementación de DIP - otros servicios dependen de esta abstracción.
    """
    
    @abstractmethod
    def fetch_data(self) -> Dict[str, Any]:
        """Obtiene datos del servicio externo"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Verifica si el servicio está disponible"""
        pass


class PartnerPropertiesService(ExternalServiceInterface):
    """
    Servicio para consumir propiedades del equipo precedente.
    
    URL ejemplo del equipo anterior: 
    https://equipo-anterior.com/api/properties/
    """
    
    def __init__(self, api_url: str = None):
        # URL del equipo precedente (reemplazar con la real)
        self.api_url = api_url or "https://jsonplaceholder.typicode.com/posts"
        self.timeout = 10
    
    def fetch_data(self) -> Dict[str, Any]:
        """Consume el servicio del equipo precedente"""
        try:
            response = requests.get(self.api_url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # Adaptar la respuesta al formato esperado
            # Si es un array, lo envolvemos en un dict
            if isinstance(data, list):
                return {
                    'success': True,
                    'count': len(data),
                    'data': data[:10],  # Limitar a 10 para ejemplo
                    'source': 'partner_api'
                }
            else:
                return {
                    'success': True,
                    'data': data,
                    'source': 'partner_api'
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'No se pudo conectar con el servicio del equipo aliado'
            }
    
    def is_available(self) -> bool:
        """Verifica si el servicio está disponible"""
        try:
            response = requests.head(self.api_url, timeout=5)
            return response.status_code < 500
        except:
            return False


class WeatherService(ExternalServiceInterface):
    """
    Servicio para consumir API del clima (ejemplo de servicio de terceros).
    
    Usando OpenWeatherMap API gratuita.
    """
    
    def __init__(self, city: str = "Bogota", api_key: str = None):
        self.city = city
        # API key de ejemplo (deberías usar una real)
        self.api_key = api_key or "demo"
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def fetch_data(self) -> Dict[str, Any]:
        """Obtiene el clima actual de la ciudad"""
        try:
            params = {
                'q': self.city,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'es'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 401:
                # API key inválida, retornar datos simulados
                return self._get_mock_weather_data()
            
            response.raise_for_status()
            data = response.json()
            
            return {
                'success': True,
                'city': data.get('name', self.city),
                'temperature': data.get('main', {}).get('temp'),
                'description': data.get('weather', [{}])[0].get('description'),
                'humidity': data.get('main', {}).get('humidity'),
                'icon': data.get('weather', [{}])[0].get('icon'),
                'source': 'openweathermap'
            }
            
        except requests.exceptions.RequestException:
            # Si falla, retornar datos simulados
            return self._get_mock_weather_data()
    
    def _get_mock_weather_data(self) -> Dict[str, Any]:
        """Datos simulados del clima para cuando la API no está disponible"""
        return {
            'success': True,
            'city': self.city,
            'temperature': 18,
            'description': 'Parcialmente nublado',
            'humidity': 65,
            'icon': '02d',
            'source': 'mock_data',
            'note': 'Datos simulados - API key no configurada'
        }
    
    def is_available(self) -> bool:
        """Verifica si el servicio está disponible"""
        try:
            response = requests.head(self.base_url, timeout=5)
            return response.status_code < 500
        except:
            return False


class ExternalServiceFactory:
    """
    Factory para crear instancias de servicios externos.
    Facilita el testing y permite cambiar implementaciones.
    """
    
    @staticmethod
    def create_partner_service(api_url: str = None) -> ExternalServiceInterface:
        """Crea servicio de propiedades aliadas"""
        return PartnerPropertiesService(api_url)
    
    @staticmethod
    def create_weather_service(city: str = "Bogota", api_key: str = None) -> ExternalServiceInterface:
        """Crea servicio del clima"""
        return WeatherService(city, api_key)
