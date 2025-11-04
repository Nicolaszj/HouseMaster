from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from property.models import Property
from datetime import timedelta


class Visit(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_COMPLETED = 'completed'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_CONFIRMED, 'Confirmada'),
        (STATUS_CANCELLED, 'Cancelada'),
        (STATUS_COMPLETED, 'Completada'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visits')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='visits')
    date_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    notes = models.TextField(blank=True, help_text="Notas adicionales sobre la visita")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'
        ordering = ["-date_time", "-created_at"]
        indexes = [
            models.Index(fields=["property", "date_time"]),
            models.Index(fields=["user", "date_time"]),
            models.Index(fields=["status", "date_time"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "property", "date_time"],
                name="uniq_visit_user_prop_datetime",
            )
        ]

    def __str__(self):
        return f"{self.user.username} → {self.property.title} ({self.date_time})"
    
    # Validaciones de negocio
    def clean(self):
        """Validaciones de negocio del modelo Visit"""
        errors = {}
        
        # No permitir visitas en el pasado
        if self.date_time and self.date_time < timezone.now():
            errors['date_time'] = "No se pueden programar visitas en el pasado"
        
        # Validar que la propiedad esté disponible
        if self.property and not self.property.is_available():
            errors['property'] = "La propiedad no está disponible para visitas"
        
        # No permitir múltiples visitas pendientes/confirmadas para el mismo usuario y propiedad
        if self.user and self.property and not self.pk:
            existing_visits = Visit.objects.filter(
                user=self.user,
                property=self.property,
                status__in=[self.STATUS_PENDING, self.STATUS_CONFIRMED]
            ).exists()
            
            if existing_visits:
                errors['property'] = "Ya tienes una visita pendiente o confirmada para esta propiedad"
        
        if errors:
            raise ValidationError(errors)
    
    # Métodos de negocio
    def is_pending(self):
        """Verifica si la visita está pendiente"""
        return self.status == self.STATUS_PENDING
    
    def is_confirmed(self):
        """Verifica si la visita está confirmada"""
        return self.status == self.STATUS_CONFIRMED
    
    def is_cancelled(self):
        """Verifica si la visita fue cancelada"""
        return self.status == self.STATUS_CANCELLED
    
    def is_completed(self):
        """Verifica si la visita fue completada"""
        return self.status == self.STATUS_COMPLETED
    
    def can_be_cancelled(self):
        """Verifica si la visita puede ser cancelada"""
        # Solo se pueden cancelar visitas pendientes o confirmadas que no hayan pasado
        return (
            self.status in [self.STATUS_PENDING, self.STATUS_CONFIRMED] and
            self.date_time > timezone.now()
        )
    
    def can_be_confirmed(self):
        """Verifica si la visita puede ser confirmada"""
        return self.status == self.STATUS_PENDING and self.date_time > timezone.now()
    
    def confirm(self):
        """Confirma la visita"""
        if self.can_be_confirmed():
            self.status = self.STATUS_CONFIRMED
            self.save()
            return True
        return False
    
    def cancel(self):
        """Cancela la visita"""
        if self.can_be_cancelled():
            self.status = self.STATUS_CANCELLED
            self.save()
            return True
        return False
    
    def complete(self):
        """Marca la visita como completada"""
        if self.is_confirmed() and self.date_time < timezone.now():
            self.status = self.STATUS_COMPLETED
            self.save()
            return True
        return False
    
    def is_upcoming(self):
        """Verifica si la visita es próxima (dentro de las próximas 24 horas)"""
        if self.date_time > timezone.now():
            time_until_visit = self.date_time - timezone.now()
            return time_until_visit <= timedelta(hours=24)
        return False

