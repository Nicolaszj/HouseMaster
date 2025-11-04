"""
Service Layer para la gestión de propiedades.
Implementa SRP (Single Responsibility) separando la lógica de negocio de las vistas.
Implementa DIP (Dependency Inversion) dependiendo de abstracciones (repositories).
"""
from typing import Dict, Any, Optional, List
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.core.paginator import Paginator
from ..repositories.property_repository import DjangoPropertyRepository
from ..repositories.interfaces import PropertyQueryRepository, PropertyCommandRepository


class PropertyService:
    """
    Servicio para la gestión de propiedades.
    Encapsula la lógica de negocio y coordina operaciones entre repositorios.
    
    SRP: Responsable únicamente de la lógica de negocio de propiedades.
    DIP: Depende de interfaces de repositorio, no de implementaciones concretas.
    OCP: Extensible mediante estrategias y filtros sin modificar el código base.
    """
    
    def __init__(self, repository: Optional[PropertyQueryRepository] = None):
        """
        Constructor del servicio.
        
        Args:
            repository: Repositorio de propiedades (DIP - inyección de dependencias)
        """
        self.repository = repository or DjangoPropertyRepository()
    
    # ===== Operaciones de consulta =====
    
    def get_all_properties(self, order_by: str = '-created_at') -> QuerySet:
        """
        Obtiene todas las propiedades.
        
        Args:
            order_by: Campo por el cual ordenar
        
        Returns:
            QuerySet de propiedades
        """
        return self.repository.get_all()
    
    def get_property_by_id(self, property_id: int):
        """
        Obtiene una propiedad por su ID.
        
        Args:
            property_id: ID de la propiedad
        
        Returns:
            Property object
        
        Raises:
            Http404: Si la propiedad no existe
        """
        return self.repository.get_by_id(property_id)
    
    def get_available_properties(self) -> QuerySet:
        """
        Obtiene solo las propiedades disponibles.
        
        Returns:
            QuerySet de propiedades disponibles
        """
        return self.repository.get_available()
    
    def get_agent_properties(self, agent_id: int) -> QuerySet:
        """
        Obtiene las propiedades de un agente específico.
        
        Args:
            agent_id: ID del agente
        
        Returns:
            QuerySet de propiedades del agente
        """
        return self.repository.get_by_agent(agent_id)
    
    def search_properties(self, filters: Dict[str, Any]) -> QuerySet:
        """
        Busca propiedades con filtros avanzados.
        
        Args:
            filters: Diccionario con filtros de búsqueda
                - city: str
                - department: str
                - type: str
                - min_price: int/float
                - max_price: int/float
                - min_rooms: int
                - min_bathrooms: int
                - available: bool
        
        Returns:
            QuerySet de propiedades filtradas
        """
        # Limpiar y validar filtros
        cleaned_filters = self._clean_search_filters(filters)
        
        # Ejecutar búsqueda
        return self.repository.search(cleaned_filters)
    
    def search_with_pagination(
        self, 
        filters: Dict[str, Any], 
        page: int = 1, 
        per_page: int = 9
    ) -> Paginator:
        """
        Busca propiedades con paginación.
        
        Args:
            filters: Filtros de búsqueda
            page: Número de página
            per_page: Elementos por página
        
        Returns:
            Paginator object
        """
        queryset = self.search_properties(filters)
        paginator = Paginator(queryset, per_page)
        return paginator.get_page(page)
    
    def get_properties_by_location(
        self, 
        city: Optional[str] = None, 
        department: Optional[str] = None
    ) -> QuerySet:
        """
        Obtiene propiedades por ubicación.
        
        Args:
            city: Ciudad
            department: Departamento
        
        Returns:
            QuerySet de propiedades en la ubicación especificada
        """
        return self.repository.get_by_location(city=city, department=department)
    
    def get_similar_properties(self, property_id: int, limit: int = 5) -> QuerySet:
        """
        Obtiene propiedades similares a una dada.
        
        Args:
            property_id: ID de la propiedad de referencia
            limit: Número máximo de propiedades similares
        
        Returns:
            QuerySet de propiedades similares
        """
        return self.repository.get_similar_properties(property_id, limit)
    
    def get_cities(self) -> QuerySet:
        """Obtiene lista de ciudades únicas"""
        return self.repository.get_cities()
    
    def get_departments(self) -> QuerySet:
        """Obtiene lista de departamentos únicos"""
        return self.repository.get_departments()
    
    # ===== Operaciones de escritura =====
    
    def create_property(self, property_data: Dict[str, Any]):
        """
        Crea una nueva propiedad.
        
        Args:
            property_data: Datos de la propiedad
        
        Returns:
            Property object creado
        
        Raises:
            ValidationError: Si los datos no son válidos
        """
        # Validar datos antes de crear
        self._validate_property_data(property_data)
        
        return self.repository.create(property_data)
    
    def update_property(self, property_id: int, property_data: Dict[str, Any]):
        """
        Actualiza una propiedad existente.
        
        Args:
            property_id: ID de la propiedad
            property_data: Datos actualizados
        
        Returns:
            Property object actualizado
        
        Raises:
            ValidationError: Si los datos no son válidos
        """
        # Validar datos antes de actualizar
        self._validate_property_data(property_data, is_update=True)
        
        return self.repository.update(property_id, property_data)
    
    def delete_property(self, property_id: int) -> bool:
        """
        Elimina una propiedad.
        
        Args:
            property_id: ID de la propiedad
        
        Returns:
            bool: True si se eliminó correctamente
        """
        return self.repository.delete(property_id)
    
    def mark_property_as_sold(self, property_id: int) -> bool:
        """
        Marca una propiedad como vendida.
        
        Args:
            property_id: ID de la propiedad
        
        Returns:
            bool: True si se actualizó correctamente
        """
        return self.repository.mark_as_sold(property_id)
    
    def mark_property_as_rented(self, property_id: int) -> bool:
        """
        Marca una propiedad como arrendada.
        
        Args:
            property_id: ID de la propiedad
        
        Returns:
            bool: True si se actualizó correctamente
        """
        return self.repository.mark_as_rented(property_id)
    
    def mark_property_as_available(self, property_id: int) -> bool:
        """
        Marca una propiedad como disponible.
        
        Args:
            property_id: ID de la propiedad
        
        Returns:
            bool: True si se actualizó correctamente
        """
        return self.repository.mark_as_available(property_id)
    
    # ===== Métodos de utilidad y cálculos =====
    
    def calculate_property_stats(self, property_id: int) -> Dict[str, Any]:
        """
        Calcula estadísticas y datos calculados de una propiedad.
        
        Args:
            property_id: ID de la propiedad
        
        Returns:
            Dict con estadísticas calculadas
        """
        property_obj = self.get_property_by_id(property_id)
        
        return {
            'price_per_sqm': property_obj.get_price_per_sqm(),
            'monthly_payment_20': property_obj.calculate_monthly_payment(down_payment_percent=20),
            'monthly_payment_30': property_obj.calculate_monthly_payment(down_payment_percent=30),
            'is_available': property_obj.is_available(),
            'is_for_sale': property_obj.is_for_sale(),
            'is_for_rent': property_obj.is_for_rent(),
        }
    
    # ===== Métodos privados de validación =====
    
    def _validate_property_data(self, data: Dict[str, Any], is_update: bool = False):
        """
        Valida los datos de una propiedad antes de crear/actualizar.
        
        Args:
            data: Datos a validar
            is_update: Indica si es una actualización (campos opcionales)
        
        Raises:
            ValidationError: Si los datos no son válidos
        """
        errors = {}
        
        # Validar precio
        if 'price' in data:
            if data['price'] is not None and data['price'] <= 0:
                errors['price'] = "El precio debe ser mayor a cero"
        
        # Validar área
        if 'area' in data:
            if data['area'] is not None and data['area'] <= 0:
                errors['area'] = "El área debe ser mayor a cero"
        
        # Validar habitaciones
        if 'rooms' in data:
            if data['rooms'] is not None and data['rooms'] < 1:
                errors['rooms'] = "Debe tener al menos 1 habitación"
        
        # Validar baños
        if 'bathrooms' in data:
            if data['bathrooms'] is not None and data['bathrooms'] < 1:
                errors['bathrooms'] = "Debe tener al menos 1 baño"
        
        if errors:
            raise ValidationError(errors)
    
    def _clean_search_filters(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Limpia y normaliza los filtros de búsqueda.
        
        Args:
            filters: Filtros sin limpiar
        
        Returns:
            Dict con filtros limpios
        """
        cleaned = {}
        
        # Limpiar ciudad
        if filters.get('city'):
            cleaned['city'] = str(filters['city']).strip()
        
        # Limpiar departamento
        if filters.get('department'):
            cleaned['department'] = str(filters['department']).strip()
        
        # Limpiar tipo
        if filters.get('type'):
            cleaned['type'] = str(filters['type']).strip()
        
        # Limpiar precios
        if filters.get('min_price'):
            try:
                min_price = int(filters['min_price'])
                if min_price >= 0:
                    cleaned['min_price'] = min_price
            except (ValueError, TypeError):
                pass
        
        if filters.get('max_price'):
            try:
                max_price = int(filters['max_price'])
                if max_price >= 0:
                    cleaned['max_price'] = max_price
            except (ValueError, TypeError):
                pass
        
        # Limpiar habitaciones
        if filters.get('min_rooms') or filters.get('rooms'):
            try:
                rooms = int(filters.get('min_rooms') or filters.get('rooms'))
                if rooms >= 1:
                    cleaned['min_rooms'] = rooms
            except (ValueError, TypeError):
                pass
        
        # Limpiar baños
        if filters.get('min_bathrooms') or filters.get('bathrooms'):
            try:
                bathrooms = int(filters.get('min_bathrooms') or filters.get('bathrooms'))
                if bathrooms >= 1:
                    cleaned['min_bathrooms'] = bathrooms
            except (ValueError, TypeError):
                pass
        
        # Filtro de disponibilidad
        if filters.get('available') is not None:
            cleaned['available'] = bool(filters['available'])
        
        # Filtro de estado
        if filters.get('status'):
            cleaned['status'] = str(filters['status']).strip()
        
        return cleaned
