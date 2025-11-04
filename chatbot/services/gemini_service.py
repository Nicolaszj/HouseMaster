import os
from django.conf import settings


class GeminiChatService:
    """
    Servicio para interactuar con la API de Gemini.
    Implementa SRP al encapsular toda la lógica de comunicación con Gemini.
    """
    
    def __init__(self):
        """Inicializa el servicio con la API key"""
        self.api_key = getattr(settings, 'GEMINI_API_KEY', None)
        self.model = None
        
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
            except ImportError:
                raise ImportError(
                    "La librería google-generativeai no está instalada. "
                    "Instálala con: pip install google-generativeai"
                )
    
    def is_configured(self):
        """Verifica si el servicio está configurado correctamente"""
        return self.api_key is not None and self.model is not None
    
    def get_system_prompt(self):
        """Retorna el prompt del sistema para contexto de HouseMaster"""
        return """Eres un asistente virtual de HouseMaster, una plataforma de bienes raíces.
Tu objetivo es ayudar a los usuarios con:
- Información sobre propiedades disponibles
- Proceso de compra y venta de propiedades
- Agendar visitas a propiedades
- Responder preguntas sobre el mercado inmobiliario
- Guiar a los usuarios en el uso de la plataforma

Sé amable, profesional y conciso en tus respuestas.
Si no tienes información específica sobre una propiedad, sugiere al usuario usar el buscador de la plataforma.
"""
    
    def generate_response(self, message, conversation_history=None):
        """
        Genera una respuesta usando Gemini.
        
        Args:
            message: Mensaje del usuario
            conversation_history: Lista de mensajes previos (opcional)
        
        Returns:
            str: Respuesta generada por Gemini
        """
        if not self.is_configured():
            return "Lo siento, el chatbot no está configurado correctamente. Por favor contacta al administrador."
        
        try:
            # Preparar el contexto con el historial
            if conversation_history:
                context = self.get_system_prompt() + "\n\nHistorial de conversación:\n"
                for msg in conversation_history[-10:]:  # Últimos 10 mensajes
                    role = "Usuario" if msg.role == "user" else "Asistente"
                    context += f"{role}: {msg.content}\n"
                context += f"\nUsuario: {message}\nAsistente:"
                
                response = self.model.generate_content(context)
            else:
                # Primera interacción
                full_message = self.get_system_prompt() + f"\n\nUsuario: {message}\nAsistente:"
                response = self.model.generate_content(full_message)
            
            return response.text
        
        except Exception as e:
            return f"Lo siento, ocurrió un error al procesar tu mensaje: {str(e)}"
    
    def generate_conversation_title(self, first_message):
        """
        Genera un título para la conversación basado en el primer mensaje.
        
        Args:
            first_message: Primer mensaje de la conversación
        
        Returns:
            str: Título sugerido
        """
        if not self.is_configured():
            return "Nueva conversación"
        
        try:
            prompt = f"Genera un título corto (máximo 5 palabras) para una conversación que inicia con: '{first_message[:100]}'"
            response = self.model.generate_content(prompt)
            return response.text.strip()[:50]  # Limitar a 50 caracteres
        except:
            # Si falla, usar las primeras palabras del mensaje
            return first_message[:50] + "..." if len(first_message) > 50 else first_message
