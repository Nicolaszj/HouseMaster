from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('propiedades/', views.propiedades, name='propiedades'),
    path('propiedades/<int:propiedad_id>/', views.propiedad_detalle, name='propiedad_detalle'),
    path('contacto/', views.contacto, name='contacto'),
    path('perfil/', views.perfil, name='account'),
    path('chat-api/', views.chatbot_api, name='chat_api'),
    path('chatbot/', views.chatbot_api, name='chatbot_api'),

    # 🔑 auth
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
