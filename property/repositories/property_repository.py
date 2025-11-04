"""
Implementación concreta del repositorio de propiedades usando Django ORM.
DIP (Dependency Inversion Principle): Implementación concreta de las interfaces.
"""
from typing import Dict, Any, Optional
from django.db.models import QuerySet, Q
from django.shortcuts import get_object_or_404
from ..models import Property
from .interfaces import PropertyQueryRepository, PropertyCommandRepository


class DjangoPropertyRepository(PropertyQueryRepository, PropertyCommandRepository):
    """
    Implementación concreta del repositorio de propiedades usando Django ORM.
    Implementa tanto queries como comandos.
    """
    
    # ===== PropertyQueryRepository methods =====
    
    def get_all(self) -> QuerySet:
        """Obtiene todas las propiedades ordenadas por fecha de creación"""
        return Property.objects.all().order_by('-created_at')
    
    def get_by_id(self, property_id: int) -> Property:
        """Obtiene una propiedad por ID o lanza 404"""
        return get_object_or_404(Property, pk=property_id)
    
    def get_available(self) -> QuerySet:
        """Obtiene solo propiedades disponibles"""
        return Property.objects.filter(status=Property.STATUS_AVAILABLE).order_by('-created_at')
    
    def get_by_agent(self, agent_id: int) -> QuerySet:
        """Obtiene propiedades de un agente específico"""
        return Property.objects.filter(agent_id=agent_id).order_by('-created_at')
    
    def search(self, filters: Dict[str, Any]) -> QuerySet:
        """
        Busca propiedades según múltiples filtros.
        
        Filtros soportados:
        - city: str
        - department: str
        - type: str (Venta/Arriendo)
        - min_price: int/float
        - max_price: int/float
        - min_rooms: int
        - min_bathrooms: int
        - min_area: float
        - max_area: float
        - status: str
        - available: bool
        """
        queryset = self.get_all()
        
        # Filtro por disponibilidad
        if filters.get('available'):
            queryset = queryset.filter(status=Property.STATUS_AVAILABLE)
        
        # Filtro por ciudad
        if filters.get('city'):
            queryset = queryset.filter(city__icontains=filters['city'])
        
        # Filtro por departamento
        if filters.get('department'):
            queryset = queryset.filter(department__icontains=filters['department'])
        
        # Filtro por tipo (Venta/Arriendo)
        if filters.get('type'):
            queryset = queryset.filter(type=filters['type'])
        
        # Filtro por rango de precio
        if filters.get('min_price') is not None:
            queryset = queryset.filter(price__gte=filters['min_price'])
        
        if filters.get('max_price') is not None:
            queryset = queryset.filter(price__lte=filters['max_price'])
        
        # Filtro por número de habitaciones
        if filters.get('min_rooms') is not None:
            queryset = queryset.filter(rooms__gte=filters['min_rooms'])
        
        # Filtro por número de baños
        if filters.get('min_bathrooms') is not None:
            queryset = queryset.filter(bathrooms__gte=filters['min_bathrooms'])
        
        # Filtro por área
        if filters.get('min_area') is not None:
            queryset = queryset.filter(area__gte=filters['min_area'])
        
        if filters.get('max_area') is not None:
            queryset = queryset.filter(area__lte=filters['max_area'])
        
        # Filtro por estado específico
        if filters.get('status'):
            queryset = queryset.filter(status=filters['status'])
        
        return queryset
    
    def get_by_location(self, city: str = None, department: str = None) -> QuerySet:
        """Obtiene propiedades por ubicación"""
        queryset = self.get_available()
        
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        if department:
            queryset = queryset.filter(department__icontains=department)
        
        return queryset
    
    def get_similar_properties(self, property_id: int, limit: int = 5) -> QuerySet:
        """
        Obtiene propiedades similares basándose en:
        - Mismo tipo (Venta/Arriendo)
        - Misma ciudad
        - Rango de precio similar (±30%)
        - Número de habitaciones similar (±1)
        """
        from decimal import Decimal
        
        try:
            property_obj = self.get_by_id(property_id)
        except:
            return Property.objects.none()
        
        # Calcular rango de precio (±30%)
        price_min = property_obj.price * Decimal('0.7')
        price_max = property_obj.price * Decimal('1.3')
        
        # Buscar propiedades similares
        similar = Property.objects.filter(
            type=property_obj.type,
            city=property_obj.city,
            price__gte=price_min,
            price__lte=price_max,
            rooms__gte=property_obj.rooms - 1,
            rooms__lte=property_obj.rooms + 1,
            status=Property.STATUS_AVAILABLE
        ).exclude(
            pk=property_id  # Excluir la propiedad original
        ).order_by('-created_at')[:limit]
        
        return similar
    
    # ===== PropertyCommandRepository methods =====
    
    def create(self, property_data: Dict[str, Any]) -> Property:
        """Crea una nueva propiedad"""
        property_obj = Property(**property_data)
        property_obj.full_clean()  # Ejecuta validaciones
        property_obj.save()
        return property_obj
    
    def update(self, property_id: int, property_data: Dict[str, Any]) -> Property:
        """Actualiza una propiedad existente"""
        property_obj = self.get_by_id(property_id)
        
        for key, value in property_data.items():
            setattr(property_obj, key, value)
        
        property_obj.full_clean()  # Ejecuta validaciones
        property_obj.save()
        return property_obj
    
    def delete(self, property_id: int) -> bool:
        """Elimina una propiedad"""
        try:
            property_obj = self.get_by_id(property_id)
            property_obj.delete()
            return True
        except:
            return False
    
    def mark_as_sold(self, property_id: int) -> bool:
        """Marca una propiedad como vendida"""
        try:
            property_obj = self.get_by_id(property_id)
            property_obj.mark_as_sold()
            return True
        except:
            return False
    
    def mark_as_rented(self, property_id: int) -> bool:
        """Marca una propiedad como arrendada"""
        try:
            property_obj = self.get_by_id(property_id)
            property_obj.mark_as_rented()
            return True
        except:
            return False
    
    def mark_as_available(self, property_id: int) -> bool:
        """Marca una propiedad como disponible"""
        try:
            property_obj = self.get_by_id(property_id)
            property_obj.mark_as_available()
            return True
        except:
            return False
    
    def get_cities(self) -> QuerySet:
        """Obtiene lista de ciudades únicas"""
        return Property.objects.values_list('city', flat=True).distinct().order_by('city')
    
    def get_departments(self) -> QuerySet:
        """Obtiene lista de departamentos únicos"""
        return Property.objects.values_list('department', flat=True).distinct().order_by('department')
