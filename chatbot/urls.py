from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('send/', views.send_message, name='chat_send_message'),
    path('conversations/', views.conversation_list, name='chat_conversations'),
    path('conversation/<int:conversation_id>/', views.load_conversation, name='load_conversation'),
]
