from django.contrib import admin
from .models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para Purchase"""
    
    list_display = [
        'id',
        'buyer',
        'property',
        'purchase_price',
        'payment_method',
        'status',
        'created_at',
    ]
    
    list_filter = [
        'status',
        'payment_method',
        'created_at',
    ]
    
    search_fields = [
        'buyer__username',
        'buyer__email',
        'property__title',
        'transaction_id',
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'completed_at',
        'transaction_id',
    ]
    
    fieldsets = (
        ('Información General', {
            'fields': ('buyer', 'property', 'status')
        }),
        ('Detalles de Compra', {
            'fields': ('purchase_price', 'down_payment', 'payment_method')
        }),
        ('Información de Pago', {
            'fields': ('transaction_id', 'payment_confirmation')
        }),
        ('Notas', {
            'fields': ('notes',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
    )
    
    def get_queryset(self, request):
        """Optimiza las consultas con select_related"""
        return super().get_queryset(request).select_related('buyer', 'property')

