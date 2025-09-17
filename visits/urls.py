from django.urls import path
from . import views

urlpatterns = [
    path("my-visits/", views.my_visits, name="my_visits"),
    path("visit/<int:visit_id>/confirm/", views.visit_confirm, name="visit_confirm"),
    path("visit/<int:visit_id>/cancel/", views.visit_cancel, name="visit_cancel"),
    path("schedule/<int:property_id>/", views.visit_schedule, name="visit_schedule"),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('property/<int:property_id>/favorite/add/', views.add_favorite, name='add_favorite'),
    path('property/<int:property_id>/favorite/remove/', views.remove_favorite, name='remove_favorite'),
]