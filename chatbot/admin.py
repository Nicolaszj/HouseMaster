from django.contrib import admin
from .models import ChatConversation, ChatMessage


class ChatMessageInline(admin.TabularInline):
    """Inline para mostrar mensajes en la conversación"""
    model = ChatMessage
    extra = 0
    readonly_fields = ['role', 'content', 'created_at']


@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para ChatConversation"""
    
    list_display = ['id', 'user', 'title', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'title']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ChatMessageInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para ChatMessage"""
    
    list_display = ['id', 'conversation', 'role', 'content_preview', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['content', 'conversation__title']
    readonly_fields = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Preview'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('conversation', 'conversation__user')

