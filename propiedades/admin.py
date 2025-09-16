from django.contrib import admin
from .models import Propiedad

class PropiedadAdmin(admin.ModelAdmin):
    list_display = ("titulo", "precio")  # campos a mostrar en la lista
    search_fields = ("titulo", "descripcion")

admin.site.register(Propiedad, PropiedadAdmin)
