# 🏠 HouseMaster
HouseMaster es una plataforma web para la gestión, promoción y compra de propiedades.  
Permite a los usuarios explorar propiedades, realizar compras y a los administradores gestionar todo el catálogo.
##  Características
- Registro y autenticación de usuarios
- Gestión de propiedades (crear, listar, buscar, filtrar)
- Compras de propiedades con formularios seguros
- Integración con un chatbot de soporte
- Estructura modular con apps de Django para mantener el proyecto limpio
##  Arquitectura
El proyecto está dividido en varias aplicaciones (apps) de Django:

- `core/` → configuración principal y páginas base
- `propiedades/` → manejo de propiedades (CRUD, detalle, filtros)
- `compras/` → procesos de compra y pagos
##  Requisitos
- Python 3.10+
- Django 5.x
- SQLite (por defecto) o PostgreSQL
- pip y virtualenv


##  Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/usuario/HouseMaster.git
   cd HouseMaster

python -m venv venv
source venv/bin/activate   # en Linux/Mac
venv\Scripts\activate      # en Windows

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

RUN SERVER 
python manage.py runserver
