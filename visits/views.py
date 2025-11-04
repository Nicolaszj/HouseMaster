from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.exceptions import ValidationError

from .forms import VisitScheduleForm
from .models import Visit
from property.models import Property
from .services.visit_service import VisitService


@login_required
def visit_schedule(request, property_id):
    """
    Programa una visita a una propiedad.
    Utiliza el Service Layer para la lógica de negocio.
    """
    prop = get_object_or_404(Property, pk=property_id)

    # Fecha seleccionada por GET (para recalcular slots)
    date_str = request.GET.get("date")
    if date_str:
        try:
            # interpretamos como fecha local (YYYY-MM-DD)
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            selected_date = timezone.localdate()
    else:
        selected_date = timezone.localdate()

    if request.method == "POST":
        form = VisitScheduleForm(request.POST, property_obj=prop, selected_date=selected_date)
        if form.is_valid():
            dt = form.cleaned_data["date_time"]

            # Usar el servicio para programar la visita
            service = VisitService()
            try:
                # Intentar programar la visita
                service.schedule_visit(
                    property_id=prop.id,
                    user_id=request.user.id,
                    date_time=dt,
                    notes=""
                )
                messages.success(request, "✅ Visita agendada. La verás en Mis visitas.")
                return redirect("my_visits")
            except ValidationError as e:
                # Si ya existe una visita, actualizarla
                Visit.objects.update_or_create(
                    user=request.user,
                    property=prop,
                    date_time=dt,
                    defaults={"status": Visit.STATUS_PENDING},
                )
                messages.success(request, "✅ Visita agendada. La verás en Mis visitas.")
                return redirect("my_visits")
        else:
            messages.error(request, "No se pudo agendar. Revisa el formulario.")
    else:
        form = VisitScheduleForm(property_obj=prop, selected_date=selected_date)

    return render(request, "visit_schedule.html", {
        "property": prop,
        "form": form,
        "selected_date": selected_date,
    })


@login_required
def my_visits(request):
    """
    Muestra las visitas del usuario autenticado.
    Utiliza el Service Layer para acceder a las visitas.
    """
    service = VisitService()
    visits = service.get_user_visits(
        user_id=request.user.id,
        include_past=True
    ).exclude(status=Visit.STATUS_CANCELLED)
    
    return render(request, "visit_list.html", {"visits": visits})


@login_required
def visit_cancel(request, visit_id):
    """
    Cancela una visita del usuario.
    Utiliza el Service Layer para la lógica de cancelación.
    """
    visit = get_object_or_404(Visit, pk=visit_id, user=request.user)
    
    service = VisitService()
    try:
        service.cancel_visit(visit_id)
        messages.success(request, "Tu visita fue cancelada.")
    except ValidationError as e:
        messages.error(request, str(e))
    
    return redirect("my_visits")


@login_required
def visit_confirm(request, visit_id):
    """
    Confirma una visita del usuario.
    Utiliza el Service Layer para la lógica de confirmación.
    """
    visit = get_object_or_404(Visit, pk=visit_id, user=request.user)
    
    service = VisitService()
    try:
        service.confirm_visit(visit_id)
        messages.success(request, "Tu visita fue confirmada.")
    except ValidationError as e:
        messages.error(request, str(e))
    
    return redirect("my_visits")