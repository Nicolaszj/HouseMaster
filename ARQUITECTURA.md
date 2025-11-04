# 📐 Arquitectura de Software - HouseMaster

## 🎯 Visión General

HouseMaster es una plataforma de gestión inmobiliaria que ha sido refactorizada siguiendo los principios SOLID y patrones de diseño reconocidos para mejorar su mantenibilidad, escalabilidad y calidad del código.

## 🏗️ Principios SOLID Implementados

### 1. **SRP (Single Responsibility Principle)**

Cada clase tiene una única responsabilidad bien definida:

#### **Modelos de Dominio** (`property/models.py`, `visits/models.py`)

- **Responsabilidad**: Representar entidades del dominio con su lógica de negocio inherente
- **Implementación**:
  ```python
  class Property(models.Model):
      # Validaciones de negocio
      def clean(self):
          # Valida reglas de negocio del modelo

      # Métodos de consulta
      def is_available(self):
          return self.status == self.STATUS_AVAILABLE

      # Cálculos de dominio
      def calculate_monthly_payment(self, ...):
          # Cálculo de pagos mensuales
  ```

#### **Servicios** (`property/services/`, `visits/services/`)

- **Responsabilidad**: Orquestar lógica de negocio y coordinar operaciones
- **Implementación**:
  ```python
  class PropertyService:
      def search_properties(self, filters):
          # Limpia filtros
          # Ejecuta búsqueda
          # Retorna resultados
  ```

#### **Repositorios** (`property/repositories/`)

- **Responsabilidad**: Acceso y manipulación de datos
- **Implementación**:
  ```python
  class DjangoPropertyRepository:
      def get_available(self):
          return Property.objects.filter(status='Disponible')
  ```

#### **Vistas** (`*/views.py`)

- **Responsabilidad**: Gestionar HTTP requests/responses
- **Implementación**: Delegan la lógica de negocio a los servicios

### 2. **OCP (Open/Closed Principle)**

El sistema está abierto a extensión pero cerrado a modificación:

#### **Constantes en Modelos**

```python
class Property(models.Model):
    TYPE_SALE = 'Venta'
    TYPE_RENT = 'Arriendo'
    TYPE_CHOICES = [
        (TYPE_SALE, 'Venta'),
        (TYPE_RENT, 'Arriendo'),
    ]
```

- ✅ Fácil agregar nuevos tipos sin modificar lógica existente

#### **Servicio Extensible**

```python
class PropertyService:
    def search_properties(self, filters: Dict[str, Any]):
        # Acepta filtros dinámicos sin modificar el código base
        cleaned_filters = self._clean_search_filters(filters)
        return self.repository.search(cleaned_filters)
```

- ✅ Nuevos filtros se pueden agregar sin cambiar el método principal

### 3. **LSP (Liskov Substitution Principle)**

Las implementaciones concretas pueden sustituir a sus abstracciones:

```python
# Interfaz
class PropertyQueryRepository(ABC):
    @abstractmethod
    def get_available(self) -> QuerySet:
        pass

# Implementación concreta
class DjangoPropertyRepository(PropertyQueryRepository):
    def get_available(self) -> QuerySet:
        return Property.objects.filter(status=Property.STATUS_AVAILABLE)
```

- ✅ Cualquier implementación de `PropertyQueryRepository` puede usarse intercambiablemente

### 4. **ISP (Interface Segregation Principle)**

Interfaces específicas y segregadas:

```python
# Interfaz para consultas (solo lectura)
class PropertyQueryRepository(ABC):
    @abstractmethod
    def get_all(self) -> QuerySet: pass
    @abstractmethod
    def search(self, filters) -> QuerySet: pass

# Interfaz para comandos (escritura)
class PropertyCommandRepository(ABC):
    @abstractmethod
    def create(self, data): pass
    @abstractmethod
    def update(self, id, data): pass
    @abstractmethod
    def delete(self, id): pass
```

- ✅ Los clientes solo dependen de las interfaces que necesitan
- ✅ Separación de lectura (queries) y escritura (commands)

### 5. **DIP (Dependency Inversion Principle)**

Dependencia de abstracciones, no de implementaciones concretas:

```python
class PropertyService:
    def __init__(self, repository: Optional[PropertyQueryRepository] = None):
        # Depende de la abstracción, no de la implementación
        self.repository = repository or DjangoPropertyRepository()

# En las vistas
def property_list(request):
    service = PropertyService()  # Inyección de dependencias
    properties = service.search_properties(filters)
```

- ✅ El servicio depende de la interfaz `PropertyQueryRepository`
- ✅ Fácil cambiar la implementación del repositorio sin modificar el servicio

## 🎨 Patrones de Diseño Implementados

### 1. **Repository Pattern**

**Problema**: Acceso directo a la base de datos desde las vistas mezclaba responsabilidades.

**Solución**: Capa de abstracción para el acceso a datos.

```
┌─────────────┐
│   Vista     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Servicio   │
└──────┬──────┘
       │
       ▼
┌─────────────┐      ┌──────────────────┐
│ Repositorio │◄────►│ Interfaz Repo    │
└──────┬──────┘      └──────────────────┘
       │
       ▼
┌─────────────┐
│   Modelo    │
└─────────────┘
```

**Archivos**:

- `property/repositories/interfaces.py` - Interfaces
- `property/repositories/property_repository.py` - Implementación

### 2. **Service Layer Pattern**

**Problema**: Lógica de negocio dispersa en vistas y modelos.

**Solución**: Capa de servicio que encapsula la lógica de negocio.

```python
# ANTES (en la vista)
def property_list(request):
    qs = Property.objects.all()
    if city := request.GET.get('city'):
        qs = qs.filter(city=city)
    # ... más lógica de filtrado

# DESPUÉS (usando servicio)
def property_list(request):
    service = PropertyService()
    filters = {'city': request.GET.get('city')}
    properties = service.search_properties(filters)
```

**Archivos**:

- `property/services/property_service.py`
- `visits/services/visit_service.py`

### 3. **Domain Model Pattern (Enriquecido)**

**Problema**: Modelos anémicos sin comportamiento.

**Solución**: Modelos con métodos de negocio.

```python
class Property(models.Model):
    # Antes: solo campos

    # Ahora: comportamiento de negocio
    def is_available(self): ...
    def calculate_monthly_payment(self, ...): ...
    def get_price_per_sqm(self): ...
    def mark_as_sold(self): ...
```

## 📊 Arquitectura en Capas

```
┌─────────────────────────────────────────────────┐
│              CAPA DE PRESENTACIÓN               │
│         (Templates, Views, Forms)               │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│           CAPA DE APLICACIÓN                    │
│              (Services)                         │
│  • PropertyService                              │
│  • VisitService                                 │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│            CAPA DE DOMINIO                      │
│          (Models con lógica)                    │
│  • Property (validaciones, cálculos)            │
│  • Visit (validaciones, estados)                │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│         CAPA DE INFRAESTRUCTURA                 │
│            (Repositories)                       │
│  • DjangoPropertyRepository                     │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│          CAPA DE PERSISTENCIA                   │
│              (Base de Datos)                    │
└─────────────────────────────────────────────────┘
```

## 🔄 Flujo de una Petición

### Ejemplo: Buscar propiedades

```
1. Usuario → HTTP Request (GET /properties/?city=Bogotá)
   │
2. View (property_list)
   │
   ├─► PropertyService.search_properties(filters)
       │
       ├─► _clean_search_filters(filters)  # Validación
       │
       ├─► DjangoPropertyRepository.search(cleaned_filters)
           │
           └─► Property.objects.filter(...).order_by(...)
               │
               └─► QuerySet
   │
3. Template renderizado con resultados
   │
4. ◄─ HTTP Response (HTML)
```

## 📁 Estructura de Archivos

```
HouseMaster/
│
├── property/
│   ├── models.py                 # Modelos de dominio enriquecidos
│   ├── views.py                  # Vistas que usan servicios
│   ├── forms.py                  # Formularios
│   ├── urls.py                   # Rutas
│   │
│   ├── services/                 # 🆕 Service Layer
│   │   ├── __init__.py
│   │   └── property_service.py   # Lógica de negocio
│   │
│   ├── repositories/             # 🆕 Repository Pattern
│   │   ├── __init__.py
│   │   ├── interfaces.py         # Interfaces (ISP)
│   │   └── property_repository.py # Implementación
│   │
│   └── tests.py                  # 🆕 Tests unitarios
│
├── visits/
│   ├── models.py                 # Modelo Visit enriquecido
│   ├── views.py                  # Vistas que usan servicios
│   ├── services/                 # 🆕 Service Layer
│   │   ├── __init__.py
│   │   └── visit_service.py      # Lógica de negocio de visitas
│   │
│   └── tests.py                  # 🆕 Tests unitarios
│
└── core/
    └── views.py                  # Vista home refactorizada
```

## ✅ Validaciones Implementadas

### En Modelos (Property)

```python
def clean(self):
    """Validaciones de negocio"""
    errors = {}

    if self.price <= 0:
        errors['price'] = "El precio debe ser mayor a cero"

    if self.rooms < 1:
        errors['rooms'] = "Debe tener al menos 1 habitación"

    # Validar coherencia de estado
    if self.status == STATUS_SOLD and self.type != TYPE_SALE:
        errors['status'] = "Solo propiedades en venta pueden estar vendidas"

    if errors:
        raise ValidationError(errors)
```

### En Modelos (Visit)

```python
def clean(self):
    """Validaciones de negocio"""
    errors = {}

    # No permitir visitas en el pasado
    if self.date_time < timezone.now():
        errors['date_time'] = "No se pueden programar visitas en el pasado"

    # Validar que la propiedad esté disponible
    if not self.property.is_available():
        errors['property'] = "La propiedad no está disponible para visitas"

    if errors:
        raise ValidationError(errors)
```

## 🧪 Tests Implementados

### Cobertura de Tests

- ✅ **PropertyModelTests**: Tests del modelo Property

  - Validaciones (precio, habitaciones, baños)
  - Métodos de negocio (is_available, calculate_monthly_payment)
  - Cálculos (precio por m², pagos mensuales)

- ✅ **PropertyRepositoryTests**: Tests del repositorio

  - Búsquedas por filtros
  - Queries específicas (disponibles, por agente, por ubicación)

- ✅ **PropertyServiceTests**: Tests del servicio

  - Búsqueda con filtros
  - Cálculo de estadísticas
  - Operaciones de negocio

- ✅ **VisitModelTests**: Tests del modelo Visit

  - Validaciones (fechas, duplicados)
  - Cambios de estado (confirmar, cancelar)
  - Métodos de negocio

- ✅ **VisitServiceTests**: Tests del servicio de visitas
  - Programación de visitas
  - Validaciones de negocio
  - Consultas específicas

### Ejecutar Tests

```bash
python manage.py test property
python manage.py test visits
```

## 🎓 Mejoras Implementadas según Feedback

### ✅ Violaciones SOLID Corregidas

1. **SRP**: ✅ Implementado

   - Modelos con lógica de dominio
   - Servicios con lógica de negocio
   - Repositorios para acceso a datos
   - Vistas solo gestionan HTTP

2. **OCP**: ✅ Implementado

   - Constantes para tipos y estados
   - Filtros extensibles en búsquedas
   - Servicios que aceptan estrategias

3. **LSP**: ✅ Implementado

   - Interfaces respetadas por implementaciones
   - Contratos claros en repositorios

4. **ISP**: ✅ Implementado

   - `PropertyQueryRepository` (solo lectura)
   - `PropertyCommandRepository` (solo escritura)

5. **DIP**: ✅ Implementado
   - Servicios dependen de interfaces
   - Vistas dependen de servicios
   - Inyección de dependencias

### ✅ Patrones de Diseño

- ✅ **Repository Pattern** implementado
- ✅ **Service Layer** implementado
- ✅ **Domain Model enriquecido** implementado

### ✅ Validaciones

- ✅ Validaciones en modelos con `clean()`
- ✅ Validaciones de negocio en servicios
- ✅ Mensajes de error descriptivos

### ✅ Tests

- ✅ Tests unitarios para modelos
- ✅ Tests unitarios para servicios
- ✅ Tests unitarios para repositorios
- ✅ Cobertura de casos críticos

## 🚀 Próximos Pasos Recomendados

1. **Documentación adicional**:

   - Diagramas de secuencia UML
   - Diagramas de clases UML
   - Documentación de API

2. **Mejoras técnicas**:

   - Logging estructurado
   - Manejo de errores centralizado
   - Cache para búsquedas frecuentes

3. **Funcionalidades**:
   - Sistema de notificaciones
   - Dashboard de estadísticas
   - API REST con Django REST Framework

## 📝 Conclusión

El proyecto HouseMaster ha sido refactorizado exitosamente implementando:

- ✅ Todos los principios SOLID
- ✅ Patrones de diseño reconocidos
- ✅ Separación clara de responsabilidades
- ✅ Validaciones de negocio robustas
- ✅ Cobertura de tests unitarios
- ✅ Arquitectura en capas bien definida

La nueva arquitectura facilita el mantenimiento, la extensibilidad y la calidad del código, cumpliendo con los estándares académicos y profesionales.
