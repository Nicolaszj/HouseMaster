from django.contrib import admin
from .models import Propiedad

admin.site.register(Propiedad)

class PropiedadAdmin(admin.ModelAdmin):
    list_display = ("titulo", "precio", "habitaciones", "banos", "metros_cuadrados")
    search_fields = ("titulo", "descripcion")