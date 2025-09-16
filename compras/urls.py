from django.urls import path
from . import views

urlpatterns = [
    path('comprar/<int:propiedad_id>/', views.comprar_propiedad, name='comprar_propiedad'),
]
