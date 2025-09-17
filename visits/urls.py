from django.urls import path
from . import views

urlpatterns = [
    path("my-visits/", views.my_visits, name="my_visits"),
    path("visit/<int:visit_id>/confirm/", views.visit_confirm, name="visit_confirm"),
    path("visit/<int:visit_id>/cancel/", views.visit_cancel, name="visit_cancel"),
    path("schedule/<int:property_id>/", views.visit_schedule, name="visit_schedule"),
]