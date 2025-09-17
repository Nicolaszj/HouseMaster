from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Property
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import PropertyForm


def property_list(request):
    qs = Property.objects.all().order_by('-created_at')

    # filtros
    city = request.GET.get('city')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    rooms = request.GET.get('rooms')
    ptype = request.GET.get('type')  
    if city:
        qs = qs.filter(city=city)
    if min_price and min_price.isdigit():
        if int(min_price) >= 0:
            qs = qs.filter(price__gte=int(min_price))
    if max_price and max_price.isdigit():
        if int(max_price) >= 0:
            qs = qs.filter(price__lte=int(max_price))
    if rooms and rooms.isdigit():
        if int(rooms) >= 1:
            qs = qs.filter(rooms__gte=int(rooms))
    if ptype in ("Arriendo", "Venta"):
        qs = qs.filter(type=ptype)
    cities = Property.objects.values_list("city", flat=True).distinct()

    # paginación (9 por página)
    paginator = Paginator(qs, 9)
    page = request.GET.get('page')
    properties = paginator.get_page(page)
    return render(request, "property_list.html", {
        "properties": properties,
        "cities": cities,
    })


def property_detail(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    return render(request, "property_detail.html", {"property": prop})


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

# Vista del panel que lista todas las propiedades
class PropertyListView(StaffRequiredMixin, ListView):
    model = Property
    template_name = 'property/property_panel.html'
    context_object_name = 'properties'

    def get_queryset(self):
        # Muestra solo las propiedades creadas por el agente logueado
        return Property.objects.filter(agent=self.request.user).order_by('-created_at')

# HU06: Vista para crear una nueva propiedad
class PropertyCreateView(StaffRequiredMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'property/property_form.html'
    success_url = reverse_lazy('property_panel')

    def form_valid(self, form):
        # Asigna el agente actual (el usuario logueado) a la propiedad
        form.instance.agent = self.request.user
        return super().form_valid(form)

# HU07: Vista para editar una propiedad existente
class PropertyUpdateView(StaffRequiredMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'property/property_form.html'
    success_url = reverse_lazy('property_panel')

# HU08: Vista para eliminar una propiedad
class PropertyDeleteView(StaffRequiredMixin, DeleteView):
    model = Property
    template_name = 'property/property_confirm_delete.html'
    success_url = reverse_lazy('property_panel')