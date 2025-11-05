# HouseMaster

**HouseMaster** es una plataforma web profesional para la gestión inmobiliaria que permite explorar, gestionar y programar visitas a propiedades. El proyecto ha sido desarrollado siguiendo principios SOLID y patrones de diseño reconocidos.

## Características Principales

### Para Usuarios

- **Registro y autenticación** de usuarios
- **Búsqueda avanzada** de propiedades con múltiples filtros
- **Sistema de visitas** para programar citas en propiedades
- **Favoritos** - Guardar propiedades de interés
- **Calculadora hipotecaria** integrada en cada propiedad
- **Propiedades similares** - Recomendaciones automáticas
- **Chatbot IA** - Asistente virtual con Google Gemini
- **Sistema de compras** - Gestión completa de transacciones

### Para Agentes Inmobiliarios

- **Panel de administración** para gestionar propiedades
- **CRUD completo** de propiedades
- **Dashboard** con estadísticas
- **Gestión de visitas** programadas
- **Gestión de compras** de clientes

### Nuevas Características - Entrega 2

- **Sistema i18n** - Español e Inglés (selector en navbar)
- **API REST con FastAPI** - Endpoints JSON documentados
- **Consumo de servicios externos** - Integración con APIs de terceros
- **Inversión de Dependencias** - Patrón DIP implementado
- **Docker** - Despliegue con docker-compose
- **Tests completos** - 50+ tests unitarios

### Características Técnicas

- **Principios SOLID** implementados
- **Patrones de diseño**: Repository, Service Layer, Domain Model, DIP
- **Tests unitarios** con cobertura completa (50+ tests)
- **Validaciones robustas** de negocio
- **Arquitectura en capas** bien definida
- **Internacionalización** (i18n) Español/Inglés
- **API REST** con FastAPI y documentación Swagger

## Arquitectura

El proyecto implementa una arquitectura en capas siguiendo los principios SOLID:

```
┌─────────────────────────────────────┐
│   Presentación (Views, Templates)  │
│   • i18n (ES/EN)                    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Aplicación (Services)           │
│  • PropertyService                  │
│  • VisitService                     │
│  • PurchaseService                  │
│  • ExternalServices (DIP)           │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    Dominio (Models enriquecidos)    │
│  • Property                         │
│  • Visit                            │
│  • Purchase                         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    API REST (FastAPI)               │
│  • GET /api/properties/             │
│  • GET /api/properties/for-sale/    │
│  • Documentación Swagger            │
└─────────────────────────────────────┘
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

## Tecnologías

- **Backend**: Django 5.x
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend**: HTML, CSS, JavaScript
- **Testing**: Django TestCase
- **Python**: 3.10+

## Requisitos

- Python 3.10+
- Django 5.x
- pip y virtualenv

## Instalación

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

### 4. Configurar variables de entorno (opcional)

```bash
# Copiar el archivo de ejemplo
copy .env.example .env

# Editar .env con tus configuraciones
```

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. **IMPORTANTE: Compilar traducciones para i18n**

El sistema i18n requiere compilar los archivos de traducción. Necesitas **gettext** instalado:

#### Opción A: Instalar gettext automáticamente (Windows)

```bash
.\install_gettext.bat
```

#### Opción B: Instalar manualmente

- **Windows con Chocolatey**: `choco install gettext`
- **Windows manual**: Descargar de https://github.com/mlocati/gettext-iconv-windows/releases
- **Linux**: `sudo apt-get install gettext`
- **Mac**: `brew install gettext`

Luego compilar:

```bash
python manage.py compilemessages
```

### 8. Ejecutar servidores

#### Servidor Django (puerto 8000)

```bash
python manage.py runserver
```

#### API FastAPI (puerto 8001)

```bash
python api_fastapi.py
```

**Accesos:**

- Django: http://localhost:8000/
- API FastAPI: http://localhost:8001/docs (Documentación Swagger)
- Admin: http://localhost:8000/admin

## Despliegue con Docker

### Opción 1: Script automático (Windows)

```bash
.\deploy.bat
```

### Opción 2: Manual

```bash
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

Acceder a: http://localhost:8000

## Sistema de Idiomas (i18n)

El sistema soporta **Español** e **Inglés**:

- **Cambiar idioma**: Usa el selector en el navbar
- **URLs con prefijo**: `/es/` para español, `/en/` para inglés
- **Traducciones**: 80+ strings traducidos

**Archivos de traducción:**

- `locale/en/LC_MESSAGES/django.po` - Traducciones al inglés
- Requiere compilación con `python manage.py compilemessages`

Ver documentación completa en **[I18N_README.md](I18N_README.md)**

## API REST con FastAPI

### Endpoints Disponibles

#### 1. Lista de propiedades

```bash
GET http://localhost:8001/api/properties/
GET http://localhost:8001/api/properties/?type=Venta&limit=5
```

#### 2. Propiedades en venta

```bash
GET http://localhost:8001/api/properties/for-sale/
```

#### 3. Detalle de propiedad

```bash
GET http://localhost:8001/api/properties/{id}/
```

### Documentación Interactiva

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

Ver documentación completa en **[API_SERVICIOS_README.md](API_SERVICIOS_README.md)**

## Servicios Externos

### Productos Aliados (Equipo Precedente)

http://localhost:8000/es/productos-aliados/

Consume API del equipo precedente y muestra productos.

### Widget del Clima

http://localhost:8000/es/clima/?city=Medellin

Consume OpenWeatherMap API para mostrar el clima.

**Patrón DIP implementado** con interfaces abstractas y factory pattern.

## Ejecutar Tests

```bash
# Todos los tests (50+)
python manage.py test

# Tests específicos por app
python manage.py test property
python manage.py test visits
python manage.py test purchases
python manage.py test chatbot
python manage.py test external_services

# Tests con verbose
python manage.py test -v 2

# Con cobertura
coverage run --source='.' manage.py test
coverage report
```

**Total de tests implementados: 50+**

- Property: 8 tests
- Visits: 12 tests
- Purchases: 20 tests
- Chatbot: 12 tests
- External Services: 9 tests

## Documentación

- **[ARQUITECTURA.md](ARQUITECTURA.md)** - Documentación completa de la arquitectura
- **[I18N_README.md](I18N_README.md)** - Sistema de internacionalización
- **[API_SERVICIOS_README.md](API_SERVICIOS_README.md)** - API REST y servicios externos
- **[FEEDBACK_PROFESOR.md](FEEDBACK_PROFESOR.md)** - Feedback académico y mejoras

## Principios SOLID Implementados

### SRP (Single Responsibility Principle)

- Modelos con lógica de dominio
- Servicios con lógica de negocio
- Repositorios para acceso a datos
- Vistas solo gestionan HTTP

### OCP (Open/Closed Principle)

- Constantes para tipos y estados
- Filtros extensibles en búsquedas

### LSP (Liskov Substitution Principle)

- Interfaces respetadas por implementaciones

### ISP (Interface Segregation Principle)

- `PropertyQueryRepository` (lectura)
- `PropertyCommandRepository` (escritura)

### DIP (Dependency Inversion Principle)

- Servicios dependen de interfaces
- Vistas dependen de servicios
- Inyección de dependencias

## Patrones de Diseño

- **Repository Pattern** - Abstracción del acceso a datos
- **Service Layer** - Encapsulación de lógica de negocio
- **Domain Model** - Modelos enriquecidos con comportamiento

## Funcionalidades Implementadas

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

## Equipo

- **Desarrollador**: [Tu nombre]
- **Curso**: Arquitectura de Software
- **Institución**: [Tu institución]

## Licencia

Este proyecto es parte de un trabajo académico.

## Enlaces

- **Repositorio**: https://github.com/Nicolaszj/HouseMaster
- **Documentación**: [ARQUITECTURA.md](ARQUITECTURA.md)
