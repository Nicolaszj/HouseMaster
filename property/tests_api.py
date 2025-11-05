from django.test import TestCase, Client
from django.contrib.auth.models import User
from property.models import Property
from decimal import Decimal
import json


class PropertyAPITests(TestCase):
    """Tests para la API REST de propiedades"""
    
    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
        
        # Crear agente
        self.agent = User.objects.create_user(
            username='agent',
            password='pass123',
            is_staff=True
        )
        
        # Crear propiedades de prueba
        self.property1 = Property.objects.create(
            agent=self.agent,
            title='Casa en venta',
            description='Hermosa casa',
            price=Decimal('200000.00'),
            area=150.0,
            rooms=3,
            bathrooms=2,
            address='Calle 123',
            city='Bogotá',
            department='Cundinamarca',
            type=Property.TYPE_SALE,
            status=Property.STATUS_AVAILABLE
        )
        
        self.property2 = Property.objects.create(
            agent=self.agent,
            title='Apartamento en arriendo',
            description='Apartamento moderno',
            price=Decimal('1500.00'),
            area=80.0,
            rooms=2,
            bathrooms=1,
            address='Carrera 45',
            city='Medellín',
            department='Antioquia',
            type=Property.TYPE_RENT,
            status=Property.STATUS_AVAILABLE
        )
    
    def test_properties_api_endpoint(self):
        """Test: Endpoint /api/properties/ retorna JSON"""
        response = self.client.get('/api/properties/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = json.loads(response.content)
        
        self.assertIn('count', data)
        self.assertIn('properties', data)
        self.assertEqual(data['count'], 2)
    
    def test_properties_api_filters_by_type(self):
        """Test: Filtrar propiedades por tipo"""
        response = self.client.get('/api/properties/?type=Venta')
        data = json.loads(response.content)
        
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['properties'][0]['title'], 'Casa en venta')
    
    def test_properties_api_filters_by_price(self):
        """Test: Filtrar por rango de precios"""
        response = self.client.get('/api/properties/?min_price=1000&max_price=5000')
        data = json.loads(response.content)
        
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['properties'][0]['title'], 'Apartamento en arriendo')
    
    def test_properties_api_limit(self):
        """Test: Limitar resultados"""
        response = self.client.get('/api/properties/?limit=1')
        data = json.loads(response.content)
        
        self.assertEqual(data['count'], 1)
    
    def test_properties_for_sale_api(self):
        """Test: Endpoint específico de propiedades en venta"""
        response = self.client.get('/api/properties/for-sale/')
        data = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('properties_for_sale', data)
        self.assertEqual(data['count'], 1)
    
    def test_api_documentation(self):
        """Test: Documentación de la API"""
        response = self.client.get('/api/docs/')
        data = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('api_name', data)
        self.assertIn('endpoints', data)
        self.assertEqual(data['api_name'], 'HouseMaster Properties API')
    
    def test_property_includes_url(self):
        """Test: Cada propiedad incluye URL directa"""
        response = self.client.get('/api/properties/')
        data = json.loads(response.content)
        
        property_data = data['properties'][0]
        self.assertIn('url', property_data)
        self.assertIn('/property/', property_data['url'])
    
    def test_property_includes_agent_info(self):
        """Test: Incluye información del agente"""
        response = self.client.get('/api/properties/')
        data = json.loads(response.content)
        
        property_data = data['properties'][0]
        self.assertIn('agent', property_data)
        self.assertEqual(property_data['agent']['username'], 'agent')
