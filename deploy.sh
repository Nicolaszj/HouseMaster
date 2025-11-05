#!/bin/bash

echo "🚀 Iniciando despliegue de HouseMaster con Docker..."

# Construir imágenes
echo "📦 Construyendo imágenes Docker..."
docker-compose build

# Levantar servicios
echo "🔧 Levantando servicios..."
docker-compose up -d

# Esperar a que la base de datos esté lista
echo "⏳ Esperando a que MySQL esté listo..."
sleep 15

# Ejecutar migraciones
echo "🔄 Ejecutando migraciones..."
docker-compose exec web python manage.py migrate

# Crear superusuario (opcional)
echo "👤 ¿Deseas crear un superusuario? (s/n)"
read -r crear_super
if [ "$crear_super" = "s" ]; then
    docker-compose exec web python manage.py createsuperuser
fi

# Cargar datos de ejemplo
echo "📊 ¿Deseas cargar propiedades de ejemplo? (s/n)"
read -r cargar_datos
if [ "$cargar_datos" = "s" ]; then
    docker-compose exec web python manage.py load_properties
fi

echo "✅ Despliegue completado!"
echo "🌐 Accede a la aplicación en: http://localhost:8000"
echo "🔧 Panel admin: http://localhost:8000/admin"
echo ""
echo "Comandos útiles:"
echo "  Ver logs: docker-compose logs -f"
echo "  Detener: docker-compose down"
echo "  Reiniciar: docker-compose restart"
