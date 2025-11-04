# Guía Rápida - Entrega 2

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Ejecutar tests
python manage.py test purchases chatbot
```

### 2. Configurar Gemini API (Opcional)

```bash
# Windows
set GEMINI_API_KEY=tu-api-key-aqui

# Linux/Mac
export GEMINI_API_KEY=tu-api-key-aqui
```

Obtener API key gratuita: https://makersuite.google.com/app/apikey

### 3. Ejecutar

```bash
python manage.py runserver
```

---

## 📱 Usar las Nuevas Funcionalidades

### Sistema de Compras

1. **Iniciar sesión** como usuario (no staff)
2. **Buscar una propiedad** en venta
3. Click en **"💳 Comprar Propiedad"**
4. **Seleccionar método de pago** y cuota inicial
5. **Confirmar compra**
6. Ver en **"Compras"** (navbar)

### Chatbot

1. **Iniciar sesión**
2. Click en **"💬 Chat"** (navbar)
3. **Escribir mensaje** en el chat
4. Esperar respuesta del asistente
5. Historial se guarda automáticamente

---

## 🧪 Tests

```bash
# Todos los tests
python manage.py test

# Solo purchases
python manage.py test purchases

# Solo chatbot
python manage.py test chatbot

# Con detalle
python manage.py test --verbosity=2
```

**Resultado esperado**: 28 tests pasando ✅

---

## 📂 Archivos Principales

### Compras

- `purchases/models.py` - Modelo Purchase
- `purchases/services/purchase_service.py` - Lógica de negocio
- `purchases/views.py` - Vistas
- `purchases/templates/purchases/` - Templates

### Chatbot

- `chatbot/models.py` - Modelos Chat
- `chatbot/services/gemini_service.py` - Servicio Gemini
- `chatbot/views.py` - Vistas
- `chatbot/templates/chatbot/chat.html` - Interfaz

---

## 🔧 Configuración

### settings.py

```python
INSTALLED_APPS = [
    # ...
    'purchases',
    'chatbot',
]

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
```

### urls.py

```python
urlpatterns = [
    # ...
    path('purchases/', include('purchases.urls')),
    path('chat/', include('chatbot.urls')),
]
```

---

## ✅ Checklist de Verificación

- [ ] `pip install -r requirements.txt` ejecutado
- [ ] `python manage.py migrate` ejecutado
- [ ] `python manage.py test` pasa 28 tests
- [ ] `python manage.py check` sin errores
- [ ] Gemini API key configurada (opcional)
- [ ] Servidor ejecutándose en http://localhost:8000

---

## 🆘 Troubleshooting

### Problema: Tests fallan

**Solución**:

```bash
python manage.py migrate
python manage.py test --verbosity=2
```

### Problema: Chatbot no responde

**Solución**:

1. Verificar `GEMINI_API_KEY` configurada
2. Verificar conexión a internet
3. Si no tienes API key, el chatbot muestra mensaje informativo

### Problema: No aparece botón "Comprar"

**Solución**:

1. Iniciar sesión como usuario (no staff)
2. Buscar propiedad con `type='Venta'`
3. La propiedad debe tener `status='Disponible'`

---

## 📊 Estadísticas del Proyecto

**Entrega 2**:

- ✅ 2 apps nuevas (purchases, chatbot)
- ✅ 3 modelos nuevos
- ✅ 2 servicios de negocio
- ✅ 8 vistas nuevas
- ✅ 5 templates nuevos
- ✅ 28 tests (100% passing)

**Total Proyecto**:

- 8 apps Django
- 55+ tests unitarios
- 6 servicios de negocio
- Arquitectura SOLID completa

---

## 📞 Contacto y Soporte

**Documentación completa**:

- `ENTREGA2_README.md` - Documentación detallada
- `RESUMEN_ENTREGA2.md` - Resumen ejecutivo
- Este archivo - Guía rápida

**Recursos**:

- Gemini API: https://ai.google.dev/
- Django Docs: https://docs.djangoproject.com/

---

Última actualización: 2025
Estado: ✅ LISTO PARA ENTREGA
