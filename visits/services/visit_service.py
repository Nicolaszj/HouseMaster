"""
Service Layer para la gestión de visitas.
"""
from django.core.exceptions import ValidationError
from django.utils import timezone
from ..models import Visit
from property.models import Property
from typing import Dict, Any, Optional
from django.db.models import QuerySet


class VisitService:
    """
    Servicio para la gestión de visitas a propiedades.
    Encapsula la lógica de negocio de las visitas.
    """
    
    def schedule_visit(
        self, 
        property_id: int, 
        user_id: int, 
        date_time, 
        notes: str = ""
    ) -> Visit:
        """
        Programa una nueva visita con validaciones de negocio.
        
        Args:
            property_id: ID de la propiedad
            user_id: ID del usuario
            date_time: Fecha y hora de la visita
            notes: Notas adicionales
        
        Returns:
            Visit object creado
        
        Raises:
            ValidationError: Si las validaciones fallan
        """
        from django.contrib.auth.models import User
        
        # Validar que la propiedad existe y está disponible
        try:
            property_obj = Property.objects.get(pk=property_id)
        except Property.DoesNotExist:
            raise ValidationError("La propiedad no existe")
        
        if not property_obj.is_available():
            raise ValidationError("La propiedad no está disponible para visitas")
        
        # Validar que no hay visitas duplicadas
        existing = Visit.objects.filter(
            user_id=user_id,
            property_id=property_id,
            status__in=[Visit.STATUS_PENDING, Visit.STATUS_CONFIRMED]
        ).exists()
        
        if existing:
            raise ValidationError(
                "Ya tienes una visita pendiente o confirmada para esta propiedad"
            )
        
        # Validar que la fecha no sea en el pasado
        if date_time < timezone.now():
            raise ValidationError("No se pueden programar visitas en el pasado")
        
        # Crear la visita
        visit = Visit.objects.create(
            user_id=user_id,
            property=property_obj,
            date_time=date_time,
            notes=notes,
            status=Visit.STATUS_PENDING
        )
        
        return visit
    
    def confirm_visit(self, visit_id: int) -> Visit:
        """
        Confirma una visita pendiente.
        
        Args:
            visit_id: ID de la visita
        
        Returns:
            Visit object actualizado
        
        Raises:
            ValidationError: Si la visita no puede ser confirmada
        """
        try:
            visit = Visit.objects.get(pk=visit_id)
        except Visit.DoesNotExist:
            raise ValidationError("La visita no existe")
        
        if not visit.can_be_confirmed():
            raise ValidationError("La visita no puede ser confirmada")
        
        visit.confirm()
        return visit
    
    def cancel_visit(self, visit_id: int) -> Visit:
        """
        Cancela una visita.
        
        Args:
            visit_id: ID de la visita
        
        Returns:
            Visit object actualizado
        
        Raises:
            ValidationError: Si la visita no puede ser cancelada
        """
        try:
            visit = Visit.objects.get(pk=visit_id)
        except Visit.DoesNotExist:
            raise ValidationError("La visita no existe")
        
        if not visit.can_be_cancelled():
            raise ValidationError("La visita no puede ser cancelada")
        
        visit.cancel()
        return visit
    
    def complete_visit(self, visit_id: int) -> Visit:
        """
        Marca una visita como completada.
        
        Args:
            visit_id: ID de la visita
        
        Returns:
            Visit object actualizado
        
        Raises:
            ValidationError: Si la visita no puede ser completada
        """
        try:
            visit = Visit.objects.get(pk=visit_id)
        except Visit.DoesNotExist:
            raise ValidationError("La visita no existe")
        
        if not visit.complete():
            raise ValidationError("La visita no puede ser completada")
        
        return visit
    
    def get_user_visits(self, user_id: int, include_past: bool = True) -> QuerySet:
        """
        Obtiene las visitas de un usuario.
        
        Args:
            user_id: ID del usuario
            include_past: Incluir visitas pasadas
        
        Returns:
            QuerySet de visitas
        """
        queryset = Visit.objects.filter(user_id=user_id)
        
        if not include_past:
            queryset = queryset.filter(date_time__gte=timezone.now())
        
        return queryset.order_by('date_time')
    
    def get_property_visits(
        self, 
        property_id: int, 
        include_cancelled: bool = False
    ) -> QuerySet:
        """
        Obtiene las visitas de una propiedad.
        
        Args:
            property_id: ID de la propiedad
            include_cancelled: Incluir visitas canceladas
        
        Returns:
            QuerySet de visitas
        """
        queryset = Visit.objects.filter(property_id=property_id)
        
        if not include_cancelled:
            queryset = queryset.exclude(status=Visit.STATUS_CANCELLED)
        
        return queryset.order_by('date_time')
    
    def get_upcoming_visits(self, user_id: Optional[int] = None) -> QuerySet:
        """
        Obtiene visitas próximas (dentro de las próximas 24 horas).
        
        Args:
            user_id: Opcional, filtrar por usuario
        
        Returns:
            QuerySet de visitas próximas
        """
        from datetime import timedelta
        
        now = timezone.now()
        tomorrow = now + timedelta(hours=24)
        
        queryset = Visit.objects.filter(
            date_time__gte=now,
            date_time__lte=tomorrow,
            status__in=[Visit.STATUS_PENDING, Visit.STATUS_CONFIRMED]
        )
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset.order_by('date_time')
