from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import VisitScheduleForm
from .models import Visit
from property.models import Property


@login_required
def visit_schedule(request, property_id):
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

            # si ya había una visita (por ejemplo cancelada) en ese mismo horario, la reusamos.
            Visit.objects.update_or_create(
                user=request.user,
                property=prop,
                date_time=dt,
                defaults={"status": "pending"},
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
    visits = (
        Visit.objects
        .filter(user=request.user)
        .exclude(status="cancelled")
        .select_related("property")
        .order_by("date_time")
    )
    
    return render(request, "visit_list.html", {"visits": visits})


@login_required
def visit_cancel(request, visit_id):
    """Cancela una visita del usuario."""
    visit = get_object_or_404(Visit, pk=visit_id, user=request.user)
    visit.status = "cancelled"
    visit.save(update_fields=["status"])
    messages.success(request, "Tu visita fue cancelada.")
    return redirect("my_visits")

@login_required
def visit_confirm(request, visit_id):
    """Confirma una visita del usuario."""
    visit = get_object_or_404(Visit, pk=visit_id, user=request.user)
    visit.status = "confirmed"
    visit.save(update_fields=["status"])
    messages.success(request, "Tu visita fue confirmada.")
    return redirect("my_visits")