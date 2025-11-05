from django.urls import path
from . import api_views

app_name = 'api'

urlpatterns = [
    path('properties/', api_views.properties_api, name='properties'),
    path('properties/for-sale/', api_views.properties_for_sale_api, name='properties_for_sale'),
    path('docs/', api_views.api_documentation, name='documentation'),
]
