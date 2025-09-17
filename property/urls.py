from django.urls import path
from . import views

urlpatterns = [
    path("propiedades/", views.property_list, name="property_list"),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
]
