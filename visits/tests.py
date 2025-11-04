from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import Visit
from property.models import Property
from .services.visit_service import VisitService
from decimal import Decimal


class VisitModelTests(TestCase):
    """Tests para el modelo Visit"""
    
    def setUp(self):
        """Configuración inicial"""
        self.user = User.objects.create_user(
            username='test_user',
            password='testpass123'
        )
        
        self.agent = User.objects.create_user(
            username='agent_test',
            password='testpass123'
        )
        
        self.property = Property.objects.create(
            agent=self.agent,
            title='Casa de prueba',
            description='Casa para testing',
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
        
        self.future_datetime = timezone.now() + timedelta(days=1)
    
    def test_create_visit(self):
        """Test: Crear una visita válida"""
        visit = Visit.objects.create(
            user=self.user,
            property=self.property,
            date_time=self.future_datetime,
            status=Visit.STATUS_PENDING
        )
        
        self.assertEqual(visit.user, self.user)
        self.assertEqual(visit.property, self.property)
        self.assertTrue(visit.is_pending())
    
    def test_visit_validation_past_date(self):
        """Test: Validación de fecha en el pasado"""
        past_datetime = timezone.now() - timedelta(days=1)
        visit = Visit(
            user=self.user,
            property=self.property,
            date_time=past_datetime
        )
        
        with self.assertRaises(ValidationError) as context:
            visit.full_clean()
        
        self.assertIn('date_time', context.exception.message_dict)
    
    def test_visit_confirm(self):
        """Test: Confirmar una visita pendiente"""
        visit = Visit.objects.create(
            user=self.user,
            property=self.property,
            date_time=self.future_datetime,
            status=Visit.STATUS_PENDING
        )
        
        result = visit.confirm()
        self.assertTrue(result)
        self.assertTrue(visit.is_confirmed())
    
    def test_visit_cancel(self):
        """Test: Cancelar una visita"""
        visit = Visit.objects.create(
            user=self.user,
            property=self.property,
            date_time=self.future_datetime,
            status=Visit.STATUS_PENDING
        )
        
        result = visit.cancel()
        self.assertTrue(result)
        self.assertTrue(visit.is_cancelled())
    
    def test_is_upcoming(self):
        """Test: Verificar si una visita es próxima"""
        # Visita en 12 horas (debe ser upcoming)
        upcoming_visit = Visit.objects.create(
            user=self.user,
            property=self.property,
            date_time=timezone.now() + timedelta(hours=12),
            status=Visit.STATUS_CONFIRMED
        )
        
        self.assertTrue(upcoming_visit.is_upcoming())
        
        # Visita en 2 días (no debe ser upcoming)
        far_visit = Visit.objects.create(
            user=self.user,
            property=self.property,
            date_time=timezone.now() + timedelta(days=2),
            status=Visit.STATUS_CONFIRMED
        )
        
        self.assertFalse(far_visit.is_upcoming())


class VisitServiceTests(TestCase):
    """Tests para el servicio de visitas"""
    
    def setUp(self):
        """Configuración inicial"""
        self.user = User.objects.create_user(
            username='test_user',
            password='testpass123'
        )
        
        self.agent = User.objects.create_user(
            username='agent_test',
            password='testpass123'
        )
        
        self.property = Property.objects.create(
            agent=self.agent,
            title='Casa de prueba',
            description='Casa para testing',
            price=Decimal('100000000'),
            type=Property.TYPE_SALE,
            area=100,
            rooms=3,
            bathrooms=2,
            status=Property.STATUS_AVAILABLE,
            city='Bogotá',
            department='Cundinamarca',
            address='Calle Test Service'
        )
        
        self.service = VisitService()
        self.future_datetime = timezone.now() + timedelta(days=1)
    
    def test_schedule_visit_success(self):
        """Test: Programar una visita exitosamente"""
        visit = self.service.schedule_visit(
            property_id=self.property.id,
            user_id=self.user.id,
            date_time=self.future_datetime,
            notes="Primera visita"
        )
        
        self.assertIsNotNone(visit)
        self.assertEqual(visit.user, self.user)
        self.assertEqual(visit.property, self.property)
        self.assertTrue(visit.is_pending())
    
    def test_schedule_visit_past_date_fails(self):
        """Test: Programar visita en el pasado debe fallar"""
        past_datetime = timezone.now() - timedelta(days=1)
        
        with self.assertRaises(ValidationError):
            self.service.schedule_visit(
                property_id=self.property.id,
                user_id=self.user.id,
                date_time=past_datetime
            )
    
    def test_schedule_duplicate_visit_fails(self):
        """Test: No permitir visitas duplicadas"""
        # Primera visita
        self.service.schedule_visit(
            property_id=self.property.id,
            user_id=self.user.id,
            date_time=self.future_datetime
        )
        
        # Intentar crear otra visita para la misma propiedad
        with self.assertRaises(ValidationError):
            self.service.schedule_visit(
                property_id=self.property.id,
                user_id=self.user.id,
                date_time=self.future_datetime + timedelta(hours=1)
            )
    
    def test_confirm_visit_service(self):
        """Test: Confirmar visita a través del servicio"""
        visit = Visit.objects.create(
            user=self.user,
            property=self.property,
            date_time=self.future_datetime,
            status=Visit.STATUS_PENDING
        )
        
        confirmed_visit = self.service.confirm_visit(visit.id)
        self.assertTrue(confirmed_visit.is_confirmed())
    
    def test_cancel_visit_service(self):
        """Test: Cancelar visita a través del servicio"""
        visit = Visit.objects.create(
            user=self.user,
            property=self.property,
            date_time=self.future_datetime,
            status=Visit.STATUS_PENDING
        )
        
        cancelled_visit = self.service.cancel_visit(visit.id)
        self.assertTrue(cancelled_visit.is_cancelled())
    
    def test_get_user_visits(self):
        """Test: Obtener visitas de un usuario"""
        Visit.objects.create(
            user=self.user,
            property=self.property,
            date_time=self.future_datetime,
            status=Visit.STATUS_PENDING
        )
        
        visits = self.service.get_user_visits(self.user.id)
        self.assertEqual(visits.count(), 1)
    
    def test_get_upcoming_visits(self):
        """Test: Obtener visitas próximas"""
        # Visita en 12 horas
        Visit.objects.create(
            user=self.user,
            property=self.property,
            date_time=timezone.now() + timedelta(hours=12),
            status=Visit.STATUS_CONFIRMED
        )
        
        # Visita en 2 días
        Visit.objects.create(
            user=self.user,
            property=self.property,
            date_time=timezone.now() + timedelta(days=2),
            status=Visit.STATUS_CONFIRMED
        )
        
        upcoming = self.service.get_upcoming_visits()
        self.assertEqual(upcoming.count(), 1)

