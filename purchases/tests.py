from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from property.models import Property
from .models import Purchase
from .services import PurchaseService
from decimal import Decimal


class PurchaseModelTests(TestCase):
    """Tests para el modelo Purchase"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear usuarios
        self.buyer = User.objects.create_user(username='buyer', password='pass123')
        self.agent = User.objects.create_user(username='agent', password='pass123', is_staff=True)
        
        # Crear propiedad
        self.property = Property.objects.create(
            agent=self.agent,
            title='Casa de prueba',
            description='Descripción',
            price=Decimal('100000.00'),
            area=100.0,
            rooms=3,
            bathrooms=2,
            address='Calle 123',
            city='Bogotá',
            department='Cundinamarca',
            type=Property.TYPE_SALE,
            status=Property.STATUS_AVAILABLE
        )
    
    def test_create_purchase_success(self):
        """Test: Crear una compra exitosamente"""
        purchase = Purchase.objects.create(
            buyer=self.buyer,
            property=self.property,
            purchase_price=self.property.price,
            down_payment=Decimal('20000.00'),
            payment_method=Purchase.PAYMENT_CREDIT_CARD
        )
        
        self.assertEqual(purchase.buyer, self.buyer)
        self.assertEqual(purchase.property, self.property)
        self.assertEqual(purchase.status, Purchase.STATUS_PENDING)
        self.assertTrue(purchase.is_pending())
    
    def test_purchase_validation_agent_cannot_buy_own_property(self):
        """Test: El agente no puede comprar su propia propiedad"""
        purchase = Purchase(
            buyer=self.agent,  # Mismo usuario que el agente
            property=self.property,
            purchase_price=self.property.price,
            payment_method=Purchase.PAYMENT_CASH
        )
        
        with self.assertRaises(ValidationError) as context:
            purchase.full_clean()
        
        self.assertIn('buyer', context.exception.message_dict)
    
    def test_purchase_validation_down_payment_exceeds_price(self):
        """Test: La cuota inicial no puede exceder el precio"""
        purchase = Purchase(
            buyer=self.buyer,
            property=self.property,
            purchase_price=Decimal('100000.00'),
            down_payment=Decimal('150000.00'),  # Mayor al precio
            payment_method=Purchase.PAYMENT_CASH
        )
        
        with self.assertRaises(ValidationError) as context:
            purchase.full_clean()
        
        self.assertIn('down_payment', context.exception.message_dict)
    
    def test_purchase_validation_negative_price(self):
        """Test: El precio de compra no puede ser negativo"""
        purchase = Purchase(
            buyer=self.buyer,
            property=self.property,
            purchase_price=Decimal('-100.00'),
            payment_method=Purchase.PAYMENT_CASH
        )
        
        with self.assertRaises(ValidationError):
            purchase.full_clean()
    
    def test_get_remaining_amount(self):
        """Test: Cálculo del monto restante"""
        purchase = Purchase.objects.create(
            buyer=self.buyer,
            property=self.property,
            purchase_price=Decimal('100000.00'),
            down_payment=Decimal('20000.00'),
            payment_method=Purchase.PAYMENT_CASH
        )
        
        self.assertEqual(purchase.get_remaining_amount(), Decimal('80000.00'))
    
    def test_get_down_payment_percentage(self):
        """Test: Cálculo del porcentaje de cuota inicial"""
        purchase = Purchase.objects.create(
            buyer=self.buyer,
            property=self.property,
            purchase_price=Decimal('100000.00'),
            down_payment=Decimal('20000.00'),
            payment_method=Purchase.PAYMENT_CASH
        )
        
        self.assertEqual(purchase.get_down_payment_percentage(), Decimal('20.00'))
    
    def test_approve_purchase(self):
        """Test: Aprobar una compra pendiente"""
        purchase = Purchase.objects.create(
            buyer=self.buyer,
            property=self.property,
            purchase_price=self.property.price,
            payment_method=Purchase.PAYMENT_CASH
        )
        
        self.assertTrue(purchase.can_be_approved())
        result = purchase.approve()
        
        self.assertTrue(result)
        self.assertTrue(purchase.is_approved())
        self.assertEqual(purchase.status, Purchase.STATUS_APPROVED)
    
    def test_complete_purchase(self):
        """Test: Completar una compra aprobada"""
        purchase = Purchase.objects.create(
            buyer=self.buyer,
            property=self.property,
            purchase_price=self.property.price,
            payment_method=Purchase.PAYMENT_CASH
        )
        
        purchase.approve()
        result = purchase.complete()
        
        self.assertTrue(result)
        self.assertTrue(purchase.is_completed())
        self.assertIsNotNone(purchase.completed_at)
        
        # Verificar que la propiedad se marcó como vendida
        self.property.refresh_from_db()
        self.assertEqual(self.property.status, Property.STATUS_SOLD)
    
    def test_cancel_purchase(self):
        """Test: Cancelar una compra"""
        purchase = Purchase.objects.create(
            buyer=self.buyer,
            property=self.property,
            purchase_price=self.property.price,
            payment_method=Purchase.PAYMENT_CASH
        )
        
        result = purchase.cancel()
        
        self.assertTrue(result)
        self.assertTrue(purchase.is_cancelled())
        self.assertEqual(purchase.status, Purchase.STATUS_CANCELLED)
    
    def test_generate_transaction_id(self):
        """Test: Generar ID de transacción"""
        purchase = Purchase.objects.create(
            buyer=self.buyer,
            property=self.property,
            purchase_price=self.property.price,
            payment_method=Purchase.PAYMENT_CASH
        )
        
        transaction_id = purchase.generate_transaction_id()
        
        self.assertIsNotNone(transaction_id)
        self.assertTrue(transaction_id.startswith('TXN-'))
        self.assertEqual(len(transaction_id), 16)  # TXN- + 12 caracteres


class PurchaseServiceTests(TestCase):
    """Tests para PurchaseService"""
    
    def setUp(self):
        """Configuración inicial"""
        self.service = PurchaseService()
        self.buyer = User.objects.create_user(username='buyer', password='pass123')
        self.agent = User.objects.create_user(username='agent', password='pass123', is_staff=True)
        
        self.property = Property.objects.create(
            agent=self.agent,
            title='Casa de prueba',
            description='Descripción',
            price=Decimal('100000.00'),
            area=100.0,
            rooms=3,
            bathrooms=2,
            address='Calle 123 Test',
            city='Bogotá',
            department='Cundinamarca',
            type=Property.TYPE_SALE,
            status=Property.STATUS_AVAILABLE
        )
    
    def test_create_purchase_service(self):
        """Test: Crear compra usando el servicio"""
        purchase = self.service.create_purchase(
            buyer=self.buyer,
            property_obj=self.property,
            payment_method=Purchase.PAYMENT_CREDIT_CARD,
            down_payment=Decimal('20000.00'),
            notes='Compra de prueba'
        )
        
        self.assertIsNotNone(purchase)
        self.assertEqual(purchase.buyer, self.buyer)
        self.assertEqual(purchase.purchase_price, self.property.price)
        self.assertIsNotNone(purchase.transaction_id)
    
    def test_create_purchase_invalid_property(self):
        """Test: No se puede comprar propiedad no disponible"""
        self.property.status = Property.STATUS_SOLD
        self.property.save()
        
        with self.assertRaises(ValidationError):
            self.service.create_purchase(
                buyer=self.buyer,
                property_obj=self.property,
                payment_method=Purchase.PAYMENT_CASH
            )
    
    def test_get_user_purchases(self):
        """Test: Obtener compras de un usuario"""
        # Crear varias compras
        for i in range(3):
            self.service.create_purchase(
                buyer=self.buyer,
                property_obj=self.property,
                payment_method=Purchase.PAYMENT_CASH
            )
        
        purchases = self.service.get_user_purchases(self.buyer)
        self.assertEqual(purchases.count(), 3)
    
    def test_approve_purchase_service(self):
        """Test: Aprobar compra usando servicio"""
        purchase = self.service.create_purchase(
            buyer=self.buyer,
            property_obj=self.property,
            payment_method=Purchase.PAYMENT_CASH
        )
        
        result = self.service.approve_purchase(purchase)
        
        self.assertTrue(result)
        purchase.refresh_from_db()
        self.assertEqual(purchase.status, Purchase.STATUS_APPROVED)
    
    def test_complete_purchase_service(self):
        """Test: Completar compra usando servicio"""
        purchase = self.service.create_purchase(
            buyer=self.buyer,
            property_obj=self.property,
            payment_method=Purchase.PAYMENT_CASH
        )
        
        self.service.approve_purchase(purchase)
        result = self.service.complete_purchase(purchase)
        
        self.assertTrue(result)
        purchase.refresh_from_db()
        self.assertEqual(purchase.status, Purchase.STATUS_COMPLETED)
    
    def test_get_purchase_statistics(self):
        """Test: Obtener estadísticas de compras"""
        # Crear compras con diferentes estados
        p1 = self.service.create_purchase(
            buyer=self.buyer,
            property_obj=self.property,
            payment_method=Purchase.PAYMENT_CASH
        )
        
        p2 = self.service.create_purchase(
            buyer=self.buyer,
            property_obj=self.property,
            payment_method=Purchase.PAYMENT_CASH
        )
        self.service.approve_purchase(p2)
        
        stats = self.service.get_purchase_statistics(self.buyer)
        
        self.assertEqual(stats['total_purchases'], 2)
        self.assertEqual(stats['pending'], 1)
        self.assertEqual(stats['approved'], 1)
        self.assertEqual(stats['completed'], 0)


class AgentPurchaseViewTests(TestCase):
    """Tests para las vistas de gestión de compras por agentes"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear usuarios
        self.buyer = User.objects.create_user(username='buyer', password='pass123')
        self.agent = User.objects.create_user(username='agent', password='pass123', is_staff=True)
        self.other_agent = User.objects.create_user(username='other_agent', password='pass123', is_staff=True)
        
        # Crear propiedades
        self.property = Property.objects.create(
            agent=self.agent,
            title='Casa del agente',
            description='Descripción',
            price=Decimal('100000.00'),
            area=100.0,
            rooms=3,
            bathrooms=2,
            address='Calle 123',
            city='Bogotá',
            department='Cundinamarca',
            type=Property.TYPE_SALE,
            status=Property.STATUS_AVAILABLE
        )
        
        # Crear compra
        self.purchase = Purchase.objects.create(
            buyer=self.buyer,
            property=self.property,
            purchase_price=self.property.price,
            down_payment=Decimal('20000.00'),
            payment_method=Purchase.PAYMENT_CREDIT_CARD,
            status=Purchase.STATUS_PENDING
        )
    
    def test_agent_purchases_view(self):
        """Test: Vista de compras del agente"""
        self.client.login(username='agent', password='pass123')
        response = self.client.get('/purchases/agent/purchases/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Casa del agente')
        self.assertContains(response, 'buyer')
    
    def test_approve_purchase_view(self):
        """Test: Aprobar compra desde la vista"""
        self.client.login(username='agent', password='pass123')
        response = self.client.post(f'/purchases/agent/approve/{self.purchase.id}/')
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.purchase.refresh_from_db()
        self.assertEqual(self.purchase.status, Purchase.STATUS_APPROVED)
    
    def test_reject_purchase_view(self):
        """Test: Rechazar compra desde la vista"""
        self.client.login(username='agent', password='pass123')
        response = self.client.post(
            f'/purchases/agent/reject/{self.purchase.id}/',
            {'reason': 'No cumple requisitos'}
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.purchase.refresh_from_db()
        self.assertEqual(self.purchase.status, Purchase.STATUS_CANCELLED)
        self.assertIn('No cumple requisitos', self.purchase.notes)
    
    def test_agent_cannot_approve_others_property_purchase(self):
        """Test: Un agente no puede aprobar compras de propiedades de otro agente"""
        self.client.login(username='other_agent', password='pass123')
        response = self.client.post(f'/purchases/agent/approve/{self.purchase.id}/')
        
        self.assertEqual(response.status_code, 404)  # Not found
        self.purchase.refresh_from_db()
        self.assertEqual(self.purchase.status, Purchase.STATUS_PENDING)  # Sin cambios

