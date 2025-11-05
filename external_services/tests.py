from django.test import TestCase, Client
from external_services.services import (
    PartnerPropertiesService,
    WeatherService,
    ExternalServiceFactory
)


class ExternalServicesTests(TestCase):
    """Tests para servicios externos"""
    
    def setUp(self):
        self.client = Client()
    
    def test_partner_service_interface(self):
        """Test: Servicio aliado implementa la interfaz correctamente"""
        service = PartnerPropertiesService()
        
        # Debe tener los métodos de la interfaz
        self.assertTrue(hasattr(service, 'fetch_data'))
        self.assertTrue(hasattr(service, 'is_available'))
    
    def test_partner_service_fetch_data(self):
        """Test: Obtener datos del servicio aliado"""
        service = PartnerPropertiesService()
        result = service.fetch_data()
        
        self.assertIn('success', result)
        self.assertIn('data', result)
        
        if result['success']:
            self.assertIn('count', result)
            self.assertIn('source', result)
    
    def test_weather_service_interface(self):
        """Test: Servicio del clima implementa la interfaz"""
        service = WeatherService()
        
        self.assertTrue(hasattr(service, 'fetch_data'))
        self.assertTrue(hasattr(service, 'is_available'))
    
    def test_weather_service_fetch_data(self):
        """Test: Obtener datos del clima"""
        service = WeatherService(city='Bogota')
        result = service.fetch_data()
        
        self.assertIn('success', result)
        self.assertIn('city', result)
        self.assertIn('temperature', result)
        self.assertIn('description', result)
    
    def test_weather_service_mock_data(self):
        """Test: Servicio retorna datos mock cuando API falla"""
        service = WeatherService(api_key='invalid_key')
        result = service.fetch_data()
        
        # Debe retornar datos simulados
        self.assertTrue(result['success'])
        self.assertEqual(result['source'], 'mock_data')
    
    def test_external_service_factory(self):
        """Test: Factory crea servicios correctamente"""
        partner_service = ExternalServiceFactory.create_partner_service()
        weather_service = ExternalServiceFactory.create_weather_service()
        
        self.assertIsInstance(partner_service, PartnerPropertiesService)
        self.assertIsInstance(weather_service, WeatherService)
    
    def test_partner_products_view(self):
        """Test: Vista de productos aliados carga correctamente"""
        response = self.client.get('/es/productos-aliados/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Productos de Nuestros Aliados')
    
    def test_weather_widget_view(self):
        """Test: Vista del widget del clima"""
        response = self.client.get('/es/clima/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Clima en')
    
    def test_weather_widget_with_custom_city(self):
        """Test: Widget del clima con ciudad personalizada"""
        response = self.client.get('/es/clima/?city=Medellin')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Medellin')
