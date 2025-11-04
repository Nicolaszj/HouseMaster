"""
Repositorios para el manejo de datos de propiedades.
Implementa el patrón Repository para abstraer el acceso a datos.
"""
from .interfaces import PropertyQueryRepository, PropertyCommandRepository
from .property_repository import DjangoPropertyRepository

__all__ = [
    'PropertyQueryRepository',
    'PropertyCommandRepository',
    'DjangoPropertyRepository',
]
