from django.contrib import admin
from .models import Visit

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'date_time', 'status', 'created_at')
    search_fields = ('user__username', 'property__title')
    list_filter = ('status', 'date_time')