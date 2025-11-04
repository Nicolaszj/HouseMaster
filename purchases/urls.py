from django.urls import path
from . import views

urlpatterns = [
    path('initiate/<int:property_id>/', views.initiate_purchase, name='initiate_purchase'),
    path('confirmation/<int:purchase_id>/', views.purchase_confirmation, name='purchase_confirmation'),
    path('my-purchases/', views.my_purchases, name='my_purchases'),
    path('cancel/<int:purchase_id>/', views.cancel_purchase, name='cancel_purchase'),
    
    # Rutas para agentes
    path('agent/purchases/', views.agent_purchases, name='agent_purchases'),
    path('agent/approve/<int:purchase_id>/', views.approve_purchase, name='approve_purchase'),
    path('agent/reject/<int:purchase_id>/', views.reject_purchase, name='reject_purchase'),
]
