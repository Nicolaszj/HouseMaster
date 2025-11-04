from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Property
from .services.property_service import PropertyService
from .repositories.property_repository import DjangoPropertyRepository


class PropertyModelTests(TestCase):
    """Tests para el modelo Property"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.user = User.objects.create_user(
            username='agent_test',
            email='agent@test.com',
            password='testpass123'
        )
        
        self.property_data = {
            'agent': self.user,
            'title': 'Casa de prueba',
            'description': 'Una casa para testing',
            'price': Decimal('150000000'),
            'type': Property.TYPE_SALE,
            'area': 120.5,
            'rooms': 3,
            'bathrooms': 2,
            'status': Property.STATUS_AVAILABLE,
            'city': 'Bogotá',
            'department': 'Cundinamarca',
            'address': 'Calle 123 #45-67'
        }
    
    def test_create_property_valid(self):
        """Test: Crear una propiedad con datos válidos"""
        property = Property.objects.create(**self.property_data)
        self.assertEqual(property.title, 'Casa de prueba')
        self.assertEqual(property.price, Decimal('150000000'))
        self.assertTrue(property.is_available())
        self.assertTrue(property.is_for_sale())
    
    def test_property_validation_negative_price(self):
        """Test: Validación de precio negativo debe fallar"""
        self.property_data['price'] = Decimal('-1000')
        property = Property(**self.property_data)
        
        with self.assertRaises(ValidationError) as context:
            property.full_clean()
        
        self.assertIn('price', context.exception.message_dict)
    
    def test_property_validation_zero_rooms(self):
        """Test: Validación de 0 habitaciones debe fallar"""
        self.property_data['rooms'] = 0
        property = Property(**self.property_data)
        
        with self.assertRaises(ValidationError) as context:
            property.full_clean()
        
        self.assertIn('rooms', context.exception.message_dict)
    
    def test_property_is_available(self):
        """Test: Método is_available()"""
        property = Property.objects.create(**self.property_data)
        self.assertTrue(property.is_available())
        
        property.status = Property.STATUS_SOLD
        property.save()
        self.assertFalse(property.is_available())
    
    def test_calculate_monthly_payment(self):
        """Test: Cálculo de pago mensual"""
        property = Property.objects.create(**self.property_data)
        monthly_payment = property.calculate_monthly_payment(
            down_payment_percent=20,
            years=30,
            annual_rate=7.5
        )
        
        self.assertIsInstance(monthly_payment, Decimal)
        self.assertGreater(monthly_payment, 0)
    
    def test_get_price_per_sqm(self):
        """Test: Cálculo de precio por metro cuadrado"""
        property = Property.objects.create(**self.property_data)
        price_per_sqm = property.get_price_per_sqm()
        
        expected = (Decimal('150000000') / Decimal('120.5')).quantize(Decimal('0.01'))
        self.assertEqual(price_per_sqm, expected)
    
    def test_mark_as_sold(self):
        """Test: Marcar propiedad como vendida"""
        property = Property.objects.create(**self.property_data)
        property.mark_as_sold()
        
        property.refresh_from_db()
        self.assertEqual(property.status, Property.STATUS_SOLD)


class PropertyRepositoryTests(TestCase):
    """Tests para el repositorio de propiedades"""
    
    def setUp(self):
        """Configuración inicial"""
        self.user = User.objects.create_user(
            username='agent_test',
            password='testpass123'
        )
        
        self.repository = DjangoPropertyRepository()
        
        # Crear propiedades de prueba
        Property.objects.create(
            agent=self.user,
            title='Casa 1',
            description='Casa disponible',
            price=Decimal('100000000'),
            type=Property.TYPE_SALE,
            area=100,
            rooms=3,
            bathrooms=2,
            status=Property.STATUS_AVAILABLE,
            city='Bogotá',
            department='Cundinamarca',
            address='Calle 1'
        )
        
        Property.objects.create(
            agent=self.user,
            title='Casa 2',
            description='Casa vendida',
            price=Decimal('200000000'),
            type=Property.TYPE_SALE,
            area=150,
            rooms=4,
            bathrooms=3,
            status=Property.STATUS_SOLD,
            city='Medellín',
            department='Antioquia',
            address='Calle 2'
        )
    
    def test_get_all(self):
        """Test: Obtener todas las propiedades"""
        properties = self.repository.get_all()
        self.assertEqual(properties.count(), 2)
    
    def test_get_available(self):
        """Test: Obtener solo propiedades disponibles"""
        properties = self.repository.get_available()
        self.assertEqual(properties.count(), 1)
        self.assertEqual(properties.first().title, 'Casa 1')
    
    def test_search_by_city(self):
        """Test: Buscar por ciudad"""
        filters = {'city': 'Bogotá'}
        properties = self.repository.search(filters)
        self.assertEqual(properties.count(), 1)
        self.assertEqual(properties.first().city, 'Bogotá')
    
    def test_search_by_price_range(self):
        """Test: Buscar por rango de precio"""
        filters = {
            'min_price': Decimal('50000000'),
            'max_price': Decimal('150000000')
        }
        properties = self.repository.search(filters)
        self.assertEqual(properties.count(), 1)
    
    def test_get_by_agent(self):
        """Test: Obtener propiedades por agente"""
        properties = self.repository.get_by_agent(self.user.id)
        self.assertEqual(properties.count(), 2)


class PropertyServiceTests(TestCase):
    """Tests para el servicio de propiedades"""
    
    def setUp(self):
        """Configuración inicial"""
        self.user = User.objects.create_user(
            username='agent_test',
            password='testpass123'
        )
        
        self.service = PropertyService()
        
        Property.objects.create(
            agent=self.user,
            title='Casa de prueba',
            description='Casa disponible',
            price=Decimal('100000000'),
            type=Property.TYPE_SALE,
            area=100,
            rooms=3,
            bathrooms=2,
            status=Property.STATUS_AVAILABLE,
            city='Bogotá',
            department='Cundinamarca',
            address='Calle Test'
        )
    
    def test_get_available_properties(self):
        """Test: Obtener propiedades disponibles a través del servicio"""
        properties = self.service.get_available_properties()
        self.assertGreater(properties.count(), 0)
    
    def test_search_properties_with_filters(self):
        """Test: Buscar propiedades con filtros"""
        filters = {
            'city': 'Bogotá',
            'min_rooms': 3
        }
        properties = self.service.search_properties(filters)
        self.assertEqual(properties.count(), 1)
    
    def test_calculate_property_stats(self):
        """Test: Calcular estadísticas de propiedad"""
        property = Property.objects.first()
        stats = self.service.calculate_property_stats(property.id)
        
        self.assertIn('price_per_sqm', stats)
        self.assertIn('monthly_payment_20', stats)
        self.assertIn('is_available', stats)
        self.assertTrue(stats['is_available'])

