from django.contrib import admin

# Register your models here.
from .models import Property, Visit, PropertyImage

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'city', 'status', 'created_at')
    search_fields = ('title', 'city', 'department', 'address')
    list_filter = ('status', 'city', 'department')
    inlines = [PropertyImageInline]

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'fecha_hora', 'estado', 'created_at')
    search_fields = ('user__username', 'property__title')
    list_filter = ('estado', 'fecha_hora')

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'is_cover', 'caption')
    list_filter = ('is_cover',)
# Register your models here.
