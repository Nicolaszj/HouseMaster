# 🚀 Guía de Implementación - Mejoras HouseMaster

## ⚠️ IMPORTANTE: Pasos para Aplicar las Mejoras

Esta guía te ayudará a aplicar las mejoras implementadas en tu base de datos existente.

---

## 📋 Paso 1: Backup de la Base de Datos

**ANTES de aplicar las migraciones, haz un backup de tu base de datos:**

```bash
# Si usas SQLite (por defecto)
cp db.sqlite3 db.sqlite3.backup

# Si usas PostgreSQL
pg_dump nombre_db > backup.sql
```

---

## 🔄 Paso 2: Aplicar Migraciones

Las migraciones ya han sido creadas. Solo necesitas aplicarlas:

```bash
python manage.py migrate
```

**Salida esperada:**

```
Running migrations:
  Applying property.0002_alter_property_options_alter_property_status_and_more... OK
  Applying visits.0002_alter_visit_options_visit_notes_visit_updated_at_and_more... OK
```

---

## ✅ Paso 3: Verificar la Instalación

### 3.1 Verificar configuración

```bash
python manage.py check
```

**Debe mostrar:** `System check identified no issues (0 silenced).`

### 3.2 Ejecutar tests

```bash
# Todos los tests
python manage.py test

# Solo property
python manage.py test property

# Solo visits
python manage.py test visits
```

**Debe mostrar:** `OK` para todos los tests.

---

## 🗄️ Paso 4: Actualizar Datos Existentes (Opcional)

Si tienes datos existentes en la base de datos, es posible que necesites actualizar algunos valores:

### 4.1 Actualizar tipos de propiedades

```python
# Ejecutar en Django shell
python manage.py shell

# En el shell:
from property.models import Property

# Actualizar tipos a los nuevos valores
Property.objects.filter(type='venta').update(type=Property.TYPE_SALE)
Property.objects.filter(type='arriendo').update(type=Property.TYPE_RENT)

# Verificar
print(Property.objects.values_list('type', flat=True).distinct())
# Debe mostrar: ['Venta', 'Arriendo']
```

### 4.2 Actualizar estados de propiedades

```python
# En el shell de Django:
from property.models import Property

# Actualizar estados a los nuevos valores
Property.objects.filter(status='disponible').update(status=Property.STATUS_AVAILABLE)
Property.objects.filter(status='vendida').update(status=Property.STATUS_SOLD)
Property.objects.filter(status='arrendada').update(status=Property.STATUS_RENTED)

# Verificar
print(Property.objects.values_list('status', flat=True).distinct())
# Debe mostrar: ['Disponible', 'Vendida', 'Arrendada', 'Reservada']
```

### 4.3 Actualizar estados de visitas

```python
# En el shell de Django:
from visits.models import Visit

# Actualizar estados
Visit.objects.filter(status='pending').update(status=Visit.STATUS_PENDING)
Visit.objects.filter(status='confirmed').update(status=Visit.STATUS_CONFIRMED)
Visit.objects.filter(status='cancelled').update(status=Visit.STATUS_CANCELLED)
```

---

## 🧪 Paso 5: Probar Funcionalidades

### 5.1 Crear una propiedad de prueba

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from property.models import Property
from decimal import Decimal

# Obtener o crear un usuario
user = User.objects.first()  # o crear uno nuevo

# Crear propiedad
prop = Property.objects.create(
    agent=user,
    title='Casa de Prueba',
    description='Una hermosa casa',
    price=Decimal('150000000'),
    type=Property.TYPE_SALE,
    area=120.5,
    rooms=3,
    bathrooms=2,
    status=Property.STATUS_AVAILABLE,
    city='Bogotá',
    department='Cundinamarca',
    address='Calle Test 123'
)

# Probar métodos
print(f"Disponible: {prop.is_available()}")
print(f"Para venta: {prop.is_for_sale()}")
print(f"Pago mensual: ${prop.calculate_monthly_payment()}")
print(f"Precio/m²: ${prop.get_price_per_sqm()}")
```

### 5.2 Usar el servicio

```python
from property.services.property_service import PropertyService

service = PropertyService()

# Buscar propiedades
properties = service.search_properties({'city': 'Bogotá'})
print(f"Encontradas: {properties.count()}")

# Obtener estadísticas
if properties.exists():
    stats = service.calculate_property_stats(properties.first().id)
    print(stats)
```

---

## 🌐 Paso 6: Probar en el Navegador

### 6.1 Iniciar el servidor

```bash
python manage.py runserver
```

### 6.2 Probar URLs

- **Home**: http://localhost:8000/
- **Lista de propiedades**: http://localhost:8000/properties/
- **Admin**: http://localhost:8000/admin/

### 6.3 Verificar funcionalidades

- ✅ Búsqueda de propiedades con filtros
- ✅ Ver detalle de propiedad
- ✅ Ver estadísticas (pago mensual, precio/m²)
- ✅ Propiedades similares
- ✅ Programar visitas
- ✅ Mis visitas

---

## 🔧 Solución de Problemas

### Error: "No such column"

**Problema**: Las migraciones no se aplicaron correctamente.

**Solución**:

```bash
# Ver estado de migraciones
python manage.py showmigrations

# Aplicar migraciones pendientes
python manage.py migrate
```

### Error: "Validation Error"

**Problema**: Datos existentes no cumplen con las nuevas validaciones.

**Solución**:

```bash
python manage.py shell
```

```python
from property.models import Property

# Encontrar propiedades con problemas
problematic = Property.objects.filter(price__lte=0)
print(f"Propiedades con precio <= 0: {problematic.count()}")

# Corregir
for prop in problematic:
    prop.price = 100000000  # Valor por defecto
    prop.save()
```

### Error en Tests

**Problema**: Algunos tests fallan.

**Solución**:

```bash
# Ejecutar tests con más detalle
python manage.py test --verbosity=2

# Ver el error específico y corregir según sea necesario
```

---

## 📊 Verificación Final

### Checklist de Verificación

- [ ] Migraciones aplicadas sin errores
- [ ] `python manage.py check` sin issues
- [ ] Todos los tests pasan (27/27)
- [ ] Datos existentes actualizados
- [ ] Servidor inicia sin errores
- [ ] Búsqueda de propiedades funciona
- [ ] Detalle de propiedad muestra estadísticas
- [ ] Sistema de visitas funciona

---

## 🎓 Próximos Pasos

Una vez que todo funcione correctamente:

1. **Revisar la documentación**:

   - Leer `ARQUITECTURA.md`
   - Leer `RESUMEN_MEJORAS.md`

2. **Explorar el código**:

   - Ver `property/services/property_service.py`
   - Ver `property/repositories/property_repository.py`
   - Ver tests en `property/tests.py`

3. **Personalizar**:
   - Agregar más validaciones según necesites
   - Extender servicios con nueva funcionalidad
   - Agregar más tests

---

## 📞 Soporte

Si tienes problemas:

1. Verifica que seguiste todos los pasos
2. Lee la documentación en `ARQUITECTURA.md`
3. Revisa los tests para ver ejemplos de uso
4. Verifica los logs de error de Django

---

## ✅ ¡Listo!

Tu proyecto HouseMaster ahora tiene:

- ✅ Arquitectura SOLID
- ✅ Patrones de diseño
- ✅ Validaciones robustas
- ✅ Tests unitarios
- ✅ Documentación completa

**¡Felicitaciones! 🎉**
