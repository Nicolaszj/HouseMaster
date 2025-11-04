from django.db import models
from django.contrib.auth.models import User


class ChatConversation(models.Model):
    """Modelo para almacenar conversaciones del chatbot"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_conversations',
        verbose_name='Usuario'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Título',
        help_text='Título de la conversación'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    class Meta:
        verbose_name = 'Conversación'
        verbose_name_plural = 'Conversaciones'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class ChatMessage(models.Model):
    """Modelo para almacenar mensajes individuales"""
    
    ROLE_USER = 'user'
    ROLE_ASSISTANT = 'assistant'
    
    ROLE_CHOICES = [
        (ROLE_USER, 'Usuario'),
        (ROLE_ASSISTANT, 'Asistente'),
    ]
    
    conversation = models.ForeignKey(
        ChatConversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Conversación'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        verbose_name='Rol'
    )
    content = models.TextField(verbose_name='Contenido')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    
    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.get_role_display()} - {self.content[:50]}"

