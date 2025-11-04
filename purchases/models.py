from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from property.models import Property
from decimal import Decimal


class Purchase(models.Model):
    """
    Modelo para gestionar las compras de propiedades.
    Implementa SRP con validaciones y métodos de negocio.
    """
    
    # Estados de la compra
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_APPROVED, 'Aprobada'),
        (STATUS_REJECTED, 'Rechazada'),
        (STATUS_COMPLETED, 'Completada'),
        (STATUS_CANCELLED, 'Cancelada'),
    ]
    
    # Métodos de pago
    PAYMENT_CREDIT_CARD = 'credit_card'
    PAYMENT_DEBIT_CARD = 'debit_card'
    PAYMENT_BANK_TRANSFER = 'bank_transfer'
    PAYMENT_CASH = 'cash'
    PAYMENT_MORTGAGE = 'mortgage'
    
    PAYMENT_CHOICES = [
        (PAYMENT_CREDIT_CARD, 'Tarjeta de Crédito'),
        (PAYMENT_DEBIT_CARD, 'Tarjeta de Débito'),
        (PAYMENT_BANK_TRANSFER, 'Transferencia Bancaria'),
        (PAYMENT_CASH, 'Efectivo'),
        (PAYMENT_MORTGAGE, 'Hipoteca'),
    ]
    
    # Relaciones
    buyer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='purchases',
        verbose_name='Comprador'
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.PROTECT,
        related_name='purchases',
        verbose_name='Propiedad'
    )
    
    # Información de la compra
    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Precio de compra',
        help_text='Precio final acordado para la compra'
    )
    down_payment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0'),
        verbose_name='Cuota inicial',
        help_text='Monto de la cuota inicial'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        verbose_name='Método de pago'
    )
    
    # Estado y tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name='Estado'
    )
    
    # Información adicional
    notes = models.TextField(
        blank=True,
        verbose_name='Notas',
        help_text='Notas adicionales sobre la compra'
    )
    
    # Información de pago (ficticia para educación)
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='ID de transacción'
    )
    payment_confirmation = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Confirmación de pago'
    )
    
    # Fechas
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de completado'
    )
    
    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['buyer', 'status']),
            models.Index(fields=['property', 'status']),
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        return f"Compra #{self.id} - {self.buyer.username} → {self.property.title}"
    
    # Validaciones de negocio
    def clean(self):
        """Validaciones de negocio del modelo Purchase"""
        errors = {}
        
        # Validar que el precio de compra sea positivo
        if self.purchase_price is not None and self.purchase_price <= 0:
            errors['purchase_price'] = "El precio de compra debe ser mayor a cero"
        
        # Validar que la cuota inicial no sea mayor al precio
        if self.down_payment is not None and self.purchase_price is not None:
            if self.down_payment > self.purchase_price:
                errors['down_payment'] = "La cuota inicial no puede ser mayor al precio de compra"
            
            if self.down_payment < 0:
                errors['down_payment'] = "La cuota inicial no puede ser negativa"
        
        # Validar que la propiedad esté disponible (solo si property_id está presente)
        # Usamos property_id para evitar el error de RelatedObjectDoesNotExist
        if self.property_id:
            try:
                prop = self.property
                if not prop.is_available():
                    if not self.pk:  # Solo al crear
                        errors['property'] = "La propiedad no está disponible para compra"
                
                # Validar que sea una propiedad en venta
                if not prop.is_for_sale():
                    errors['property'] = "Solo se pueden comprar propiedades en venta"
                
                # Validar que el comprador no sea el agente de la propiedad
                if self.buyer and self.buyer == prop.agent:
                    errors['buyer'] = "No puedes comprar tu propia propiedad"
            except Property.DoesNotExist:
                errors['property'] = "La propiedad especificada no existe"
        
        if errors:
            raise ValidationError(errors)
    
    # Métodos de negocio
    def is_pending(self):
        """Verifica si la compra está pendiente"""
        return self.status == self.STATUS_PENDING
    
    def is_approved(self):
        """Verifica si la compra fue aprobada"""
        return self.status == self.STATUS_APPROVED
    
    def is_completed(self):
        """Verifica si la compra fue completada"""
        return self.status == self.STATUS_COMPLETED
    
    def is_cancelled(self):
        """Verifica si la compra fue cancelada"""
        return self.status == self.STATUS_CANCELLED
    
    def can_be_approved(self):
        """Verifica si la compra puede ser aprobada"""
        return self.status == self.STATUS_PENDING
    
    def can_be_completed(self):
        """Verifica si la compra puede ser completada"""
        return self.status == self.STATUS_APPROVED
    
    def can_be_cancelled(self):
        """Verifica si la compra puede ser cancelada"""
        return self.status in [self.STATUS_PENDING, self.STATUS_APPROVED]
    
    def approve(self):
        """Aprueba la compra"""
        if self.can_be_approved():
            self.status = self.STATUS_APPROVED
            self.save()
            return True
        return False
    
    def complete(self):
        """Completa la compra y marca la propiedad como vendida"""
        if self.can_be_completed():
            self.status = self.STATUS_COMPLETED
            self.completed_at = timezone.now()
            self.save()
            
            # Marcar la propiedad como vendida
            if self.property.is_for_sale():
                self.property.mark_as_sold()
            
            return True
        return False
    
    def cancel(self):
        """Cancela la compra"""
        if self.can_be_cancelled():
            self.status = self.STATUS_CANCELLED
            self.save()
            return True
        return False
    
    def reject(self):
        """Rechaza la compra"""
        if self.is_pending():
            self.status = self.STATUS_REJECTED
            self.save()
            return True
        return False
    
    def get_remaining_amount(self):
        """Calcula el monto restante a pagar"""
        return (self.purchase_price - self.down_payment).quantize(Decimal('0.01'))
    
    def get_down_payment_percentage(self):
        """Calcula el porcentaje de la cuota inicial"""
        if self.purchase_price > 0:
            return ((self.down_payment / self.purchase_price) * 100).quantize(Decimal('0.01'))
        return Decimal('0')
    
    def generate_transaction_id(self):
        """Genera un ID de transacción ficticio"""
        import uuid
        self.transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        self.save()
        return self.transaction_id

