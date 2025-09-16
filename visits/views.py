from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Visit

@login_required
def my_visits(request):
    visits = Visit.objects.filter(user=request.user).exclude(status="cancelled")
    return render(request, "visit_list.html", {"visits": visits})

@login_required
def visit_confirm(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id, user=request.user)
    if visit.status != "confirmed":
        visit.status = "confirmed"
        visit.save()
        messages.success(request, "Visita confirmada correctamente")
    return redirect("my_visits")

@login_required
def visit_cancel(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id, user=request.user)
    if visit.status != "cancelled":
        visit.status = "cancelled"
        visit.save()
        messages.warning(request, "Visita cancelada")
    return redirect("my_visits")