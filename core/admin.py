from django.contrib import admin
from .models import Property, Visit


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'city', 'status', 'created_at')
    search_fields = ('title', 'city', 'department', 'address')
    list_filter = ('status', 'city', 'department')


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'fecha_hora', 'estado', 'created_at')
    search_fields = ('user__username', 'property__title')
    list_filter = ('estado', 'fecha_hora')

# Register your models here.
