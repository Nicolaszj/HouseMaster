from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from property.models import Property
from .models import Purchase
from .forms import PurchaseForm
from .services import PurchaseService


purchase_service = PurchaseService()


@login_required
def initiate_purchase(request, property_id):
    """Vista para iniciar la compra de una propiedad"""
    property_obj = get_object_or_404(Property, id=property_id)
    
    # Validar que la propiedad esté disponible
    if not property_obj.is_available():
        messages.error(request, "Esta propiedad no está disponible para compra.")
        return redirect('property_detail', pk=property_id)
    
    # Validar que el usuario no sea el agente
    if request.user == property_obj.agent:
        messages.error(request, "No puedes comprar tu propia propiedad.")
        return redirect('property_detail', pk=property_id)
    
    if request.method == 'POST':
        form = PurchaseForm(request.POST, property=property_obj)
        if form.is_valid():
            try:
                # Crear la compra usando el servicio
                purchase = purchase_service.create_purchase(
                    buyer=request.user,
                    property_obj=property_obj,
                    payment_method=form.cleaned_data['payment_method'],
                    down_payment=form.cleaned_data.get('down_payment'),
                    notes=form.cleaned_data.get('notes', ''),
                )
                
                messages.success(
                    request,
                    f"¡Compra iniciada exitosamente! ID de transacción: {purchase.transaction_id}"
                )
                return redirect('purchase_confirmation', purchase_id=purchase.id)
            
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = PurchaseForm(property=property_obj)
    
    context = {
        'form': form,
        'property': property_obj,
    }
    return render(request, 'purchases/initiate_purchase.html', context)


@login_required
def purchase_confirmation(request, purchase_id):
    """Vista de confirmación de compra"""
    purchase = get_object_or_404(
        Purchase.objects.select_related('property', 'property__agent'),
        id=purchase_id,
        buyer=request.user
    )
    
    context = {
        'purchase': purchase,
    }
    return render(request, 'purchases/purchase_confirmation.html', context)


@login_required
def my_purchases(request):
    """Vista de compras del usuario"""
    purchases = purchase_service.get_user_purchases(request.user)
    stats = purchase_service.get_purchase_statistics(request.user)
    
    context = {
        'purchases': purchases,
        'stats': stats,
    }
    return render(request, 'purchases/my_purchases.html', context)


@login_required
def cancel_purchase(request, purchase_id):
    """Cancela una compra"""
    purchase = get_object_or_404(Purchase, id=purchase_id, buyer=request.user)
    
    if request.method == 'POST':
        try:
            purchase_service.cancel_purchase(purchase)
            messages.success(request, "Compra cancelada exitosamente.")
        except ValidationError as e:
            messages.error(request, str(e))
        
        return redirect('my_purchases')
    
    context = {
        'purchase': purchase,
    }
    return render(request, 'purchases/cancel_confirm.html', context)


@login_required
def agent_purchases(request):
    """Vista de compras de las propiedades del agente"""
    # Obtener todas las compras de las propiedades del agente
    purchases = Purchase.objects.filter(
        property__agent=request.user
    ).select_related('buyer', 'property').order_by('-created_at')
    
    # Estadísticas
    pending_count = purchases.filter(status=Purchase.STATUS_PENDING).count()
    approved_count = purchases.filter(status=Purchase.STATUS_APPROVED).count()
    completed_count = purchases.filter(status=Purchase.STATUS_COMPLETED).count()
    
    context = {
        'purchases': purchases,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'completed_count': completed_count,
    }
    return render(request, 'purchases/agent_purchases.html', context)


@login_required
def approve_purchase(request, purchase_id):
    """Aprueba una compra pendiente"""
    purchase = get_object_or_404(
        Purchase,
        id=purchase_id,
        property__agent=request.user
    )
    
    if request.method == 'POST':
        try:
            purchase_service.approve_purchase(purchase)
            messages.success(
                request,
                f"Compra aprobada exitosamente. El comprador {purchase.buyer.get_full_name() or purchase.buyer.username} ha sido notificado."
            )
        except ValidationError as e:
            messages.error(request, str(e))
        
        return redirect('agent_purchases')
    
    context = {
        'purchase': purchase,
        'action': 'aprobar',
    }
    return render(request, 'purchases/approve_confirm.html', context)


@login_required
def reject_purchase(request, purchase_id):
    """Rechaza una compra pendiente"""
    purchase = get_object_or_404(
        Purchase,
        id=purchase_id,
        property__agent=request.user
    )
    
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        try:
            # Cancelar la compra y agregar la razón en las notas
            if reason:
                purchase.notes = f"{purchase.notes}\n\nRazón de rechazo: {reason}".strip()
            purchase_service.cancel_purchase(purchase)
            messages.success(request, "Compra rechazada exitosamente.")
        except ValidationError as e:
            messages.error(request, str(e))
        
        return redirect('agent_purchases')
    
    context = {
        'purchase': purchase,
        'action': 'rechazar',
    }
    return render(request, 'purchases/approve_confirm.html', context)

