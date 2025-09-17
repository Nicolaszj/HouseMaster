from django.urls import path
from . import views
from .views import PropertyListView, PropertyCreateView, PropertyUpdateView, PropertyDeleteView

urlpatterns = [
    path("propiedades/", views.property_list, name="property_list"),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('panel/', PropertyListView.as_view(), name='property_panel'),
    path('panel/new/', PropertyCreateView.as_view(), name='property_create'),
    path('panel/<int:pk>/edit/', PropertyUpdateView.as_view(), name='property_update'),
    path('panel/<int:pk>/delete/', PropertyDeleteView.as_view(), name='property_delete'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('property/<int:property_id>/favorite/add/', views.add_favorite, name='add_favorite'),
    path('property/<int:property_id>/favorite/remove/', views.remove_favorite, name='remove_favorite'),
]
