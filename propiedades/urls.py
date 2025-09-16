from django.urls import path
from . import views
from compras import views as compras_views

urlpatterns = [
    path('', views.propiedades, name='propiedades'),
    path('<int:propiedad_id>/', views.propiedad_detalle, name='propiedad_detalle'),
    path('<int:propiedad_id>/comprar/', compras_views.comprar_propiedad, name='comprar_propiedad'),
]
