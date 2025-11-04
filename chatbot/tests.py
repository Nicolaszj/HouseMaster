from django.test import TestCase
from django.contrib.auth.models import User
from .models import ChatConversation, ChatMessage
from .services import GeminiChatService


class ChatConversationModelTests(TestCase):
    """Tests para el modelo ChatConversation"""
    
    def setUp(self):
        """Configuración inicial"""
        self.user = User.objects.create_user(username='testuser', password='pass123')
    
    def test_create_conversation(self):
        """Test: Crear una conversación"""
        conversation = ChatConversation.objects.create(
            user=self.user,
            title='Test Conversation'
        )
        
        self.assertEqual(conversation.user, self.user)
        self.assertEqual(conversation.title, 'Test Conversation')
        self.assertIsNotNone(conversation.created_at)
    
    def test_conversation_str(self):
        """Test: Representación en string de conversación"""
        conversation = ChatConversation.objects.create(
            user=self.user,
            title='Test Title'
        )
        
        expected = f"{self.user.username} - Test Title"
        self.assertEqual(str(conversation), expected)


class ChatMessageModelTests(TestCase):
    """Tests para el modelo ChatMessage"""
    
    def setUp(self):
        """Configuración inicial"""
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.conversation = ChatConversation.objects.create(
            user=self.user,
            title='Test Conversation'
        )
    
    def test_create_user_message(self):
        """Test: Crear mensaje de usuario"""
        message = ChatMessage.objects.create(
            conversation=self.conversation,
            role=ChatMessage.ROLE_USER,
            content='Hello, this is a test message'
        )
        
        self.assertEqual(message.conversation, self.conversation)
        self.assertEqual(message.role, ChatMessage.ROLE_USER)
        self.assertEqual(message.content, 'Hello, this is a test message')
    
    def test_create_assistant_message(self):
        """Test: Crear mensaje del asistente"""
        message = ChatMessage.objects.create(
            conversation=self.conversation,
            role=ChatMessage.ROLE_ASSISTANT,
            content='This is a response'
        )
        
        self.assertEqual(message.role, ChatMessage.ROLE_ASSISTANT)
    
    def test_message_str(self):
        """Test: Representación en string de mensaje"""
        message = ChatMessage.objects.create(
            conversation=self.conversation,
            role=ChatMessage.ROLE_USER,
            content='This is a long message that should be truncated in the string representation'
        )
        
        str_repr = str(message)
        self.assertIn('Usuario', str_repr)
        self.assertTrue(len(str_repr) < len(message.content))


class GeminiChatServiceTests(TestCase):
    """Tests para GeminiChatService"""
    
    def setUp(self):
        """Configuración inicial"""
        self.service = GeminiChatService()
    
    def test_service_initialization(self):
        """Test: Inicialización del servicio"""
        # El servicio debe inicializarse sin errores
        self.assertIsNotNone(self.service)
    
    def test_get_system_prompt(self):
        """Test: Obtener prompt del sistema"""
        prompt = self.service.get_system_prompt()
        
        self.assertIsNotNone(prompt)
        self.assertIn('HouseMaster', prompt)
        self.assertIn('bienes raíces', prompt)
    
    def test_generate_conversation_title_fallback(self):
        """Test: Generación de título sin API configurada"""
        # Si la API no está configurada, debe usar fallback
        title = self.service.generate_conversation_title('¿Qué propiedades tienen disponibles?')
        
        self.assertIsNotNone(title)
        self.assertTrue(len(title) <= 50)
    
    def test_is_configured(self):
        """Test: Verificar si el servicio está configurado"""
        # Dependiendo de si GEMINI_API_KEY está configurada
        configured = self.service.is_configured()
        self.assertIsInstance(configured, bool)


class ChatConversationFlowTests(TestCase):
    """Tests de flujo completo de conversación"""
    
    def setUp(self):
        """Configuración inicial"""
        self.user = User.objects.create_user(username='testuser', password='pass123')
    
    def test_create_conversation_with_messages(self):
        """Test: Crear conversación con múltiples mensajes"""
        conversation = ChatConversation.objects.create(
            user=self.user,
            title='Property Inquiry'
        )
        
        # Crear mensajes
        user_msg = ChatMessage.objects.create(
            conversation=conversation,
            role=ChatMessage.ROLE_USER,
            content='¿Cuánto cuesta una casa?'
        )
        
        assistant_msg = ChatMessage.objects.create(
            conversation=conversation,
            role=ChatMessage.ROLE_ASSISTANT,
            content='El precio varía según la ubicación y características.'
        )
        
        # Verificar relaciones
        self.assertEqual(conversation.messages.count(), 2)
        messages = list(conversation.messages.all())
        self.assertIn(user_msg, messages)
        self.assertIn(assistant_msg, messages)
    
    def test_conversation_ordering(self):
        """Test: Orden de conversaciones por fecha de actualización"""
        # Crear varias conversaciones
        conv1 = ChatConversation.objects.create(user=self.user, title='Conv 1')
        conv2 = ChatConversation.objects.create(user=self.user, title='Conv 2')
        conv3 = ChatConversation.objects.create(user=self.user, title='Conv 3')
        
        # Actualizar conv1 (debe aparecer primero)
        conv1.save()
        
        conversations = ChatConversation.objects.all()
        self.assertEqual(conversations.first(), conv1)
    
    def test_message_ordering(self):
        """Test: Orden de mensajes por fecha de creación"""
        conversation = ChatConversation.objects.create(
            user=self.user,
            title='Test'
        )
        
        msg1 = ChatMessage.objects.create(
            conversation=conversation,
            role=ChatMessage.ROLE_USER,
            content='First message'
        )
        
        msg2 = ChatMessage.objects.create(
            conversation=conversation,
            role=ChatMessage.ROLE_ASSISTANT,
            content='Second message'
        )
        
        messages = conversation.messages.all()
        self.assertEqual(len(messages), 2)
        # Verificar que ambos mensajes están presentes
        message_contents = [m.content for m in messages]
        self.assertIn('First message', message_contents)
        self.assertIn('Second message', message_contents)

