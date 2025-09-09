from django.urls import path
from . import views

urlpatterns = [
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
]
