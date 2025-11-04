# HouseMaster - Entrega 2

## Nuevas Funcionalidades Implementadas

### 1. Sistema de Compras de Propiedades

Se implementó un sistema completo de compras que permite a los usuarios comprar propiedades desde la plataforma.

#### Características:

- **Modelo Purchase** con estados de compra (pendiente, aprobada, completada, cancelada, rechazada)
- **Métodos de pago** ficticios: tarjeta de crédito, débito, transferencia, efectivo, hipoteca
- **Validaciones de negocio**:
  - El agente no puede comprar su propia propiedad
  - Solo se pueden comprar propiedades en venta y disponibles
  - La cuota inicial no puede ser mayor al precio
  - La propiedad se marca como vendida al completar la compra
- **Servicio PurchaseService**: Encapsula la lógica de negocio

  - `create_purchase()`: Crea una nueva compra con validaciones
  - `approve_purchase()`: Aprueba una compra pendiente
  - `complete_purchase()`: Completa la compra y marca la propiedad como vendida
  - `cancel_purchase()`: Cancela una compra
  - `get_purchase_statistics()`: Obtiene estadísticas de compras

- **Sistema de pagos educativo**:
  - Generación de ID de transacción ficticio
  - No se realizan cargos reales
  - Sistema diseñado para aprendizaje

#### Flujo de Compra:

1. Usuario autenticado ve botón "Comprar Propiedad" en propiedades en venta
2. Selecciona método de pago y cuota inicial
3. Se crea la compra en estado "pendiente"
4. Se genera ID de transacción
5. Usuario puede ver sus compras en "Mis Compras"
6. Puede cancelar compras pendientes o aprobadas

#### URLs:

- `/purchases/initiate/<property_id>/` - Iniciar compra
- `/purchases/confirmation/<purchase_id>/` - Confirmación de compra
- `/purchases/my-purchases/` - Ver mis compras
- `/purchases/cancel/<purchase_id>/` - Cancelar compra

---

### 2. Chatbot con Gemini API

Se implementó un chatbot inteligente usando la API gratuita de Google Gemini.

#### Características:

- **Modelos**:

  - `ChatConversation`: Almacena conversaciones del usuario
  - `ChatMessage`: Almacena mensajes individuales (usuario/asistente)

- **Servicio GeminiChatService**:
  - Integración con Google Gemini API
  - Prompt de sistema personalizado para HouseMaster
  - Manejo de historial de conversación
  - Generación automática de títulos para conversaciones
- **Interfaz interactiva**:
  - Chat en tiempo real con AJAX
  - Historial de conversaciones
  - Persistencia de mensajes
  - Diseño responsive

#### Configuración de Gemini API:

1. **Obtener API Key gratuita**:
   - Visita: https://makersuite.google.com/app/apikey
   - Crea una nueva API key
2. **Instalar dependencias**:

   ```bash
   pip install google-generativeai
   ```

3. **Configurar en settings.py**:

   ```python
   GEMINI_API_KEY = 'tu-api-key-aqui'
   ```

   O usar variable de entorno:

   ```bash
   set GEMINI_API_KEY=tu-api-key-aqui  # Windows
   export GEMINI_API_KEY=tu-api-key-aqui  # Linux/Mac
   ```

#### Capacidades del Chatbot:

- Responde preguntas sobre propiedades
- Ayuda con el proceso de compra/venta
- Guía en el uso de la plataforma
- Información sobre visitas
- Asistencia general sobre bienes raíces

#### URLs:

- `/chat/` - Interfaz principal del chat
- `/chat/send/` - Enviar mensaje (AJAX)
- `/chat/conversations/` - Lista de conversaciones
- `/chat/conversation/<id>/` - Cargar conversación específica

---

## Arquitectura Implementada

Ambas funcionalidades siguen los principios SOLID implementados en la Entrega 1:

### Single Responsibility Principle (SRP)

- Cada servicio tiene una única responsabilidad
- Modelos solo contienen lógica de dominio
- Vistas solo manejan HTTP

### Dependency Inversion Principle (DIP)

- Servicios desacoplados de la implementación
- Uso de inyección de dependencias

### Service Layer Pattern

- `PurchaseService`: Lógica de negocio de compras
- `GeminiChatService`: Comunicación con API externa

---

## Instalación y Uso

### 1. Instalar dependencias:

```bash
pip install -r requirements.txt
```

### 2. Aplicar migraciones:

```bash
python manage.py migrate
```

### 3. Configurar Gemini API Key (opcional):

```bash
set GEMINI_API_KEY=tu-api-key
```

### 4. Iniciar servidor:

```bash
python manage.py runserver
```

### 5. Probar funcionalidades:

- Ir a una propiedad en venta → Click en "Comprar Propiedad"
- Ir a `/chat/` para usar el chatbot

---

## Archivos Creados/Modificados

### Purchases App:

- `purchases/models.py` - Modelo Purchase
- `purchases/admin.py` - Configuración admin
- `purchases/forms.py` - PurchaseForm
- `purchases/views.py` - Vistas de compra
- `purchases/urls.py` - URLs
- `purchases/services/purchase_service.py` - Servicio de negocio
- `purchases/templates/purchases/` - Templates

### Chatbot App:

- `chatbot/models.py` - Modelos ChatConversation y ChatMessage
- `chatbot/admin.py` - Configuración admin
- `chatbot/views.py` - Vistas del chat
- `chatbot/urls.py` - URLs
- `chatbot/services/gemini_service.py` - Servicio Gemini
- `chatbot/templates/chatbot/chat.html` - Interfaz del chat

### Modificaciones:

- `HouseMaster/settings.py` - Agregadas apps y configuración Gemini
- `HouseMaster/urls.py` - Agregadas URLs de purchases y chatbot
- `property/templates/property_detail.html` - Agregado botón de compra

---

## Notas Importantes

1. **Sistema de Pagos**: Es completamente ficticio y educativo. No se realizan transacciones reales.

2. **Gemini API**:

   - Usa créditos gratuitos de Google
   - Requiere conexión a internet
   - Si no está configurado, el chatbot muestra un mensaje informativo

3. **Próximos Pasos Recomendados**:
   - Crear tests unitarios para Purchase y Chatbot
   - Agregar notificaciones cuando cambien estados de compra
   - Mejorar el prompt del chatbot con información específica de propiedades
   - Agregar manejo de errores más robusto en el chatbot

---

## Créditos

- **Google Gemini API**: Para el chatbot inteligente
- **Django 5.1**: Framework web
- **Bootstrap**: Framework CSS
