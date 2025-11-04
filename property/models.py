from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal


class Property(models.Model):
    # Constantes para choices (OCP - Open/Closed Principle)
    TYPE_SALE = 'Venta'
    TYPE_RENT = 'Arriendo'
    TYPE_CHOICES = [
        (TYPE_SALE, 'Venta'),
        (TYPE_RENT, 'Arriendo'),
    ]
    
    STATUS_AVAILABLE = 'Disponible'
    STATUS_SOLD = 'Vendida'
    STATUS_RENTED = 'Arrendada'
    STATUS_RESERVED = 'Reservada'
    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'Disponible'),
        (STATUS_SOLD, 'Vendida'),
        (STATUS_RENTED, 'Arrendada'),
        (STATUS_RESERVED, 'Reservada'),
    ]
    
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='properties')

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    area = models.FloatField()
    rooms = models.IntegerField()
    bathrooms = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)
    city = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    address = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='properties/', blank=True, null=True)

    class Meta:
        verbose_name = 'Propiedad'
        verbose_name_plural = 'Propiedades'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['city', 'type']),
            models.Index(fields=['status', 'price']),
        ]

    def __str__(self):
        return f"{self.title} - {self.city}"
    
    # SRP - Single Responsibility: Validaciones de negocio en el modelo
    def clean(self):
        """Validaciones de negocio del modelo"""
        errors = {}
        
        if self.price is not None and self.price <= 0:
            errors['price'] = "El precio debe ser mayor a cero"
        
        if self.area is not None and self.area <= 0:
            errors['area'] = "El área debe ser mayor a cero"
        
        if self.rooms is not None and self.rooms < 1:
            errors['rooms'] = "Debe tener al menos 1 habitación"
        
        if self.bathrooms is not None and self.bathrooms < 1:
            errors['bathrooms'] = "Debe tener al menos 1 baño"
        
        # Validar coherencia de estado
        if self.status == self.STATUS_SOLD and self.type != self.TYPE_SALE:
            errors['status'] = "Solo propiedades en venta pueden estar vendidas"
        
        if self.status == self.STATUS_RENTED and self.type != self.TYPE_RENT:
            errors['status'] = "Solo propiedades en arriendo pueden estar arrendadas"
        
        if errors:
            raise ValidationError(errors)
    
    # Métodos de negocio (SRP - lógica de dominio en el modelo)
    def is_available(self):
        """Verifica si la propiedad está disponible"""
        return self.status == self.STATUS_AVAILABLE
    
    def is_for_sale(self):
        """Verifica si la propiedad es para venta"""
        return self.type == self.TYPE_SALE
    
    def is_for_rent(self):
        """Verifica si la propiedad es para arriendo"""
        return self.type == self.TYPE_RENT
    
    def calculate_monthly_payment(self, down_payment_percent=20, years=30, annual_rate=7.5):
        """
        Calcula el pago mensual estimado para una propiedad en venta
        
        Args:
            down_payment_percent: Porcentaje de cuota inicial (default 20%)
            years: Años del crédito (default 30)
            annual_rate: Tasa de interés anual (default 7.5%)
        
        Returns:
            Decimal: Pago mensual estimado
        """
        if not self.is_for_sale():
            return Decimal('0')
        
        # Calcular monto del préstamo
        down_payment = self.price * Decimal(down_payment_percent / 100)
        loan_amount = self.price - down_payment
        
        # Convertir tasa anual a mensual
        monthly_rate = Decimal(annual_rate / 100 / 12)
        num_payments = years * 12
        
        # Fórmula de pago mensual: M = P * [r(1+r)^n] / [(1+r)^n - 1]
        if monthly_rate > 0:
            monthly_payment = loan_amount * (
                monthly_rate * (1 + monthly_rate) ** num_payments
            ) / (
                (1 + monthly_rate) ** num_payments - 1
            )
        else:
            monthly_payment = loan_amount / Decimal(num_payments)
        
        return monthly_payment.quantize(Decimal('0.01'))
    
    def get_price_per_sqm(self):
        """Calcula el precio por metro cuadrado"""
        if self.area > 0:
            return (self.price / Decimal(str(self.area))).quantize(Decimal('0.01'))
        return Decimal('0')
    
    def mark_as_sold(self):
        """Marca la propiedad como vendida"""
        if self.is_for_sale():
            self.status = self.STATUS_SOLD
            self.save()
    
    def mark_as_rented(self):
        """Marca la propiedad como arrendada"""
        if self.is_for_rent():
            self.status = self.STATUS_RENTED
            self.save()
    
    def mark_as_available(self):
        """Marca la propiedad como disponible"""
        self.status = self.STATUS_AVAILABLE
        self.save()


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    caption = models.CharField(max_length=150, blank=True)
    is_cover = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_cover', 'id']  # portada primero

    def __str__(self):
        return f"Foto de {self.property.title}"
