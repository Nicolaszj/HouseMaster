from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import ChatConversation, ChatMessage
from .services import GeminiChatService
import json


gemini_service = GeminiChatService()


@login_required
def chat_view(request):
    """Vista principal del chat"""
    conversations = ChatConversation.objects.filter(user=request.user)[:10]
    
    context = {
        'conversations': conversations,
        'gemini_configured': gemini_service.is_configured(),
    }
    return render(request, 'chatbot/chat.html', context)


@login_required
@require_POST
def send_message(request):
    """Envía un mensaje y obtiene respuesta del chatbot"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id')
        
        if not message:
            return JsonResponse({'error': 'El mensaje no puede estar vacío'}, status=400)
        
        with transaction.atomic():
            # Obtener o crear conversación
            if conversation_id:
                conversation = get_object_or_404(
                    ChatConversation,
                    id=conversation_id,
                    user=request.user
                )
            else:
                # Generar título para nueva conversación
                title = gemini_service.generate_conversation_title(message)
                conversation = ChatConversation.objects.create(
                    user=request.user,
                    title=title
                )
            
            # Guardar mensaje del usuario
            user_message = ChatMessage.objects.create(
                conversation=conversation,
                role=ChatMessage.ROLE_USER,
                content=message
            )
            
            # Obtener historial de la conversación
            history = list(conversation.messages.all().order_by('created_at'))
            
            # Generar respuesta con Gemini
            response_text = gemini_service.generate_response(message, history[:-1])
            
            # Guardar respuesta del asistente
            assistant_message = ChatMessage.objects.create(
                conversation=conversation,
                role=ChatMessage.ROLE_ASSISTANT,
                content=response_text
            )
        
        return JsonResponse({
            'success': True,
            'conversation_id': conversation.id,
            'user_message': {
                'id': user_message.id,
                'content': user_message.content,
                'created_at': user_message.created_at.isoformat(),
            },
            'assistant_message': {
                'id': assistant_message.id,
                'content': assistant_message.content,
                'created_at': assistant_message.created_at.isoformat(),
            }
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def conversation_list(request):
    """Lista las conversaciones del usuario"""
    conversations = ChatConversation.objects.filter(user=request.user)
    
    data = [{
        'id': conv.id,
        'title': conv.title,
        'created_at': conv.created_at.isoformat(),
        'updated_at': conv.updated_at.isoformat(),
    } for conv in conversations]
    
    return JsonResponse({'conversations': data})


@login_required
def load_conversation(request, conversation_id):
    """Carga una conversación específica"""
    conversation = get_object_or_404(
        ChatConversation,
        id=conversation_id,
        user=request.user
    )
    
    messages = [{
        'id': msg.id,
        'role': msg.role,
        'content': msg.content,
        'created_at': msg.created_at.isoformat(),
    } for msg in conversation.messages.all()]
    
    return JsonResponse({
        'conversation': {
            'id': conversation.id,
            'title': conversation.title,
            'created_at': conversation.created_at.isoformat(),
        },
        'messages': messages
    })

