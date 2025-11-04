from django.db import transaction
from django.core.exceptions import ValidationError
from ..models import Purchase
from property.models import Property
from decimal import Decimal


class PurchaseService:
    """
    Servicio que encapsula la lógica de negocio de compras.
    Implementa SRP y facilita testing con DIP.
    """
    
    @transaction.atomic
    def create_purchase(self, buyer, property_obj, payment_method, down_payment=None, notes=''):
        """
        Crea una nueva compra de propiedad.
        
        Args:
            buyer: Usuario comprador
            property_obj: Propiedad a comprar
            payment_method: Método de pago seleccionado
            down_payment: Cuota inicial (opcional)
            notes: Notas adicionales (opcional)
        
        Returns:
            Purchase: Instancia de compra creada
        
        Raises:
            ValidationError: Si la compra no puede realizarse
        """
        # Validar que la propiedad existe y está disponible
        if not property_obj.is_available():
            raise ValidationError("La propiedad no está disponible para compra")
        
        # Validar que sea una propiedad en venta
        if not property_obj.is_for_sale():
            raise ValidationError("Solo se pueden comprar propiedades en venta")
        
        # Validar que el comprador no sea el agente
        if buyer == property_obj.agent:
            raise ValidationError("No puedes comprar tu propia propiedad")
        
        # Establecer valores por defecto
        if down_payment is None:
            down_payment = Decimal('0')
        
        # Crear la compra
        purchase = Purchase(
            buyer=buyer,
            property=property_obj,
            purchase_price=property_obj.price,
            down_payment=down_payment,
            payment_method=payment_method,
            notes=notes,
        )
        
        # Validar modelo
        purchase.full_clean()
        purchase.save()
        
        # Generar ID de transacción ficticio
        purchase.generate_transaction_id()
        
        return purchase
    
    def get_user_purchases(self, user, status=None):
        """
        Obtiene las compras de un usuario.
        
        Args:
            user: Usuario comprador
            status: Estado de compra (opcional)
        
        Returns:
            QuerySet: Compras del usuario
        """
        queryset = Purchase.objects.filter(buyer=user).select_related('property', 'property__agent')
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')
    
    def get_property_purchases(self, property_obj, status=None):
        """
        Obtiene las compras de una propiedad.
        
        Args:
            property_obj: Propiedad
            status: Estado de compra (opcional)
        
        Returns:
            QuerySet: Compras de la propiedad
        """
        queryset = Purchase.objects.filter(property=property_obj).select_related('buyer')
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')
    
    @transaction.atomic
    def approve_purchase(self, purchase):
        """
        Aprueba una compra pendiente.
        
        Args:
            purchase: Instancia de Purchase
        
        Returns:
            bool: True si se aprobó, False si no
        """
        if not purchase.can_be_approved():
            raise ValidationError("La compra no puede ser aprobada en su estado actual")
        
        return purchase.approve()
    
    @transaction.atomic
    def complete_purchase(self, purchase):
        """
        Completa una compra aprobada.
        
        Args:
            purchase: Instancia de Purchase
        
        Returns:
            bool: True si se completó, False si no
        """
        if not purchase.can_be_completed():
            raise ValidationError("La compra no puede ser completada en su estado actual")
        
        return purchase.complete()
    
    @transaction.atomic
    def cancel_purchase(self, purchase):
        """
        Cancela una compra.
        
        Args:
            purchase: Instancia de Purchase
        
        Returns:
            bool: True si se canceló, False si no
        """
        if not purchase.can_be_cancelled():
            raise ValidationError("La compra no puede ser cancelada en su estado actual")
        
        return purchase.cancel()
    
    def get_purchase_statistics(self, user=None):
        """
        Obtiene estadísticas de compras.
        
        Args:
            user: Usuario (opcional, si None devuelve estadísticas globales)
        
        Returns:
            dict: Diccionario con estadísticas
        """
        queryset = Purchase.objects.all()
        
        if user:
            queryset = queryset.filter(buyer=user)
        
        total_purchases = queryset.count()
        pending_purchases = queryset.filter(status=Purchase.STATUS_PENDING).count()
        approved_purchases = queryset.filter(status=Purchase.STATUS_APPROVED).count()
        completed_purchases = queryset.filter(status=Purchase.STATUS_COMPLETED).count()
        cancelled_purchases = queryset.filter(status=Purchase.STATUS_CANCELLED).count()
        
        # Calcular monto total de compras completadas
        completed = queryset.filter(status=Purchase.STATUS_COMPLETED)
        total_amount = sum(p.purchase_price for p in completed) if completed.exists() else Decimal('0')
        
        return {
            'total_purchases': total_purchases,
            'pending': pending_purchases,
            'approved': approved_purchases,
            'completed': completed_purchases,
            'cancelled': cancelled_purchases,
            'total_amount': total_amount,
        }
