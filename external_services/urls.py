from django.urls import path
from . import views

urlpatterns = [
    path('productos-aliados/', views.partner_products, name='partner_products'),
    path('clima/', views.weather_widget, name='weather_widget'),
]
