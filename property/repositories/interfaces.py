"""
Interfaces para los repositorios de propiedades.
Implementa ISP (Interface Segregation Principle) separando lecturas de escrituras.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from django.db.models import QuerySet


class PropertyQueryRepository(ABC):
    """
    Interfaz para operaciones de solo lectura (queries) de propiedades.
    ISP: Interfaz segregada para consultas.
    """
    
    @abstractmethod
    def get_all(self) -> QuerySet:
        """Obtiene todas las propiedades"""
        pass
    
    @abstractmethod
    def get_by_id(self, property_id: int):
        """Obtiene una propiedad por ID"""
        pass
    
    @abstractmethod
    def get_available(self) -> QuerySet:
        """Obtiene propiedades disponibles"""
        pass
    
    @abstractmethod
    def get_by_agent(self, agent_id: int) -> QuerySet:
        """Obtiene propiedades de un agente específico"""
        pass
    
    @abstractmethod
    def search(self, filters: Dict[str, Any]) -> QuerySet:
        """Busca propiedades según filtros"""
        pass
    
    @abstractmethod
    def get_by_location(self, city: str = None, department: str = None) -> QuerySet:
        """Obtiene propiedades por ubicación"""
        pass
    
    @abstractmethod
    def get_similar_properties(self, property_id: int, limit: int = 5) -> QuerySet:
        """Obtiene propiedades similares a una dada"""
        pass


class PropertyCommandRepository(ABC):
    """
    Interfaz para operaciones de escritura de propiedades.
    ISP: Interfaz segregada para comandos.
    """
    
    @abstractmethod
    def create(self, property_data: Dict[str, Any]):
        """Crea una nueva propiedad"""
        pass
    
    @abstractmethod
    def update(self, property_id: int, property_data: Dict[str, Any]):
        """Actualiza una propiedad existente"""
        pass
    
    @abstractmethod
    def delete(self, property_id: int) -> bool:
        """Elimina una propiedad"""
        pass
    
    @abstractmethod
    def mark_as_sold(self, property_id: int) -> bool:
        """Marca una propiedad como vendida"""
        pass
    
    @abstractmethod
    def mark_as_rented(self, property_id: int) -> bool:
        """Marca una propiedad como arrendada"""
        pass
    
    @abstractmethod
    def mark_as_available(self, property_id: int) -> bool:
        """Marca una propiedad como disponible"""
        pass
