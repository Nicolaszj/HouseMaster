from django.urls import path
from . import views

urlpatterns = [
    # Página principal
    path('', views.home, name='home'),

    # Propiedades
    path('propiedades/', views.propiedades, name='propiedades'),
    path('propiedades/<int:propiedad_id>/', views.propiedad_detalle, name='propiedad_detalle'),
    path('propiedades/<int:propiedad_id>/comprar/', views.comprar_propiedad, name='comprar_propiedad'),

    # Contacto
    path('contacto/', views.contacto, name='contacto'),

    # Perfil
    path('perfil/', views.perfil, name='perfil'),

    # Chatbot
    path('chat-api/', views.chatbot_api, name='chat_api'),
    path('chatbot/', views.chatbot_api, name='chatbot_api'),

    # Autenticación
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
