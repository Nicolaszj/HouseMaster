# 🏠 HouseMaster

**HouseMaster** es una plataforma web profesional para la gestión inmobiliaria que permite explorar, gestionar y programar visitas a propiedades. El proyecto ha sido desarrollado siguiendo principios SOLID y patrones de diseño reconocidos.

## ✨ Características Principales

### Para Usuarios

- 🔐 **Registro y autenticación** de usuarios
- 🔍 **Búsqueda avanzada** de propiedades con múltiples filtros
- 📅 **Sistema de visitas** para programar citas en propiedades
- ⭐ **Favoritos** - Guardar propiedades de interés
- 💰 **Calculadora hipotecaria** integrada en cada propiedad
- 📊 **Propiedades similares** - Recomendaciones automáticas

### Para Agentes Inmobiliarios

- 📝 **Panel de administración** para gestionar propiedades
- ✏️ **CRUD completo** de propiedades
- 📈 **Dashboard** con estadísticas
- 👥 **Gestión de visitas** programadas

### Características Técnicas

- ✅ **Principios SOLID** implementados
- 🎨 **Patrones de diseño**: Repository, Service Layer, Domain Model
- 🧪 **Tests unitarios** con cobertura completa
- 🔒 **Validaciones robustas** de negocio
- 📐 **Arquitectura en capas** bien definida

## 🏗️ Arquitectura

El proyecto implementa una arquitectura en capas siguiendo los principios SOLID:

```
┌─────────────────────────────────────┐
│   Presentación (Views, Templates)  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Aplicación (Services)           │
│  • PropertyService                  │
│  • VisitService                     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    Dominio (Models enriquecidos)    │
│  • Property                         │
│  • Visit                            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Infraestructura (Repositories)     │
│  • DjangoPropertyRepository         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Persistencia (Database)        │
└─────────────────────────────────────┘
```

### Estructura del Proyecto

```
HouseMaster/
│
├── property/                # App de propiedades
│   ├── models.py           # Modelos de dominio enriquecidos
│   ├── views.py            # Vistas que usan servicios
│   ├── services/           # 🆕 Service Layer
│   │   └── property_service.py
│   ├── repositories/       # 🆕 Repository Pattern
│   │   ├── interfaces.py
│   │   └── property_repository.py
│   └── tests.py            # 🆕 Tests unitarios
│
├── visits/                 # App de visitas
│   ├── models.py           # Modelo Visit enriquecido
│   ├── views.py            # Vistas que usan servicios
│   ├── services/           # 🆕 Service Layer
│   │   └── visit_service.py
│   └── tests.py            # 🆕 Tests unitarios
│
├── account/                # App de cuentas de usuario
├── core/                   # App central
└── HouseMaster/            # Configuración del proyecto
```

## 🛠️ Tecnologías

- **Backend**: Django 5.x
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend**: HTML, CSS, JavaScript
- **Testing**: Django TestCase
- **Python**: 3.10+

## 📋 Requisitos

- Python 3.10+
- Django 5.x
- pip y virtualenv

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Nicolaszj/HouseMaster.git
cd HouseMaster
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

### 6. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

Acceder a: `http://localhost:8000`

## 🧪 Ejecutar Tests

```bash
# Todos los tests
python manage.py test

# Tests específicos
python manage.py test property
python manage.py test visits

# Con cobertura
coverage run --source='.' manage.py test
coverage report
```

## 📚 Documentación

- **[ARQUITECTURA.md](ARQUITECTURA.md)** - Documentación completa de la arquitectura
- **[FEEDBACK_PROFESOR.md](FEEDBACK_PROFESOR.md)** - Feedback académico y mejoras

## 🎯 Principios SOLID Implementados

### ✅ SRP (Single Responsibility Principle)

- Modelos con lógica de dominio
- Servicios con lógica de negocio
- Repositorios para acceso a datos
- Vistas solo gestionan HTTP

### ✅ OCP (Open/Closed Principle)

- Constantes para tipos y estados
- Filtros extensibles en búsquedas

### ✅ LSP (Liskov Substitution Principle)

- Interfaces respetadas por implementaciones

### ✅ ISP (Interface Segregation Principle)

- `PropertyQueryRepository` (lectura)
- `PropertyCommandRepository` (escritura)

### ✅ DIP (Dependency Inversion Principle)

- Servicios dependen de interfaces
- Vistas dependen de servicios
- Inyección de dependencias

## 🎨 Patrones de Diseño

- ✅ **Repository Pattern** - Abstracción del acceso a datos
- ✅ **Service Layer** - Encapsulación de lógica de negocio
- ✅ **Domain Model** - Modelos enriquecidos con comportamiento

## 📊 Funcionalidades Implementadas

### Gestión de Propiedades

- [x] Crear, editar y eliminar propiedades
- [x] Búsqueda avanzada con filtros múltiples
- [x] Paginación de resultados
- [x] Propiedades similares
- [x] Calculadora hipotecaria
- [x] Sistema de favoritos

### Gestión de Visitas

- [x] Programar visitas a propiedades
- [x] Confirmar/cancelar visitas
- [x] Validación de fechas y disponibilidad
- [x] Listado de visitas del usuario

### Validaciones

- [x] Validación de precios positivos
- [x] Validación de habitaciones/baños mínimos
- [x] Coherencia entre tipo y estado de propiedad
- [x] Validación de fechas de visitas
- [x] Prevención de visitas duplicadas

## 👥 Equipo

- **Desarrollador**: [Tu nombre]
- **Curso**: Arquitectura de Software
- **Institución**: [Tu institución]

## 📄 Licencia

Este proyecto es parte de un trabajo académico.

## 🔗 Enlaces

- **Repositorio**: https://github.com/Nicolaszj/HouseMaster
- **Documentación**: [ARQUITECTURA.md](ARQUITECTURA.md)
