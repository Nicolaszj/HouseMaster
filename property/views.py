from django.shortcuts import render, get_object_or_404, redirect
from .models import Property
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PropertyForm
from django.contrib.auth.decorators import login_required
from .services.property_service import PropertyService


def property_list(request):
    """
    Lista de propiedades con filtros y paginación.
    Utiliza Service Layer para separar la lógica de negocio.
    """
    # Inicializar servicio
    service = PropertyService()
    
    # Obtener filtros del request
    filters = {
        'city': request.GET.get('city'),
        'min_price': request.GET.get('min_price'),
        'max_price': request.GET.get('max_price'),
        'rooms': request.GET.get('rooms'),
        'type': request.GET.get('type'),
    }
    
    # Buscar propiedades con paginación usando el servicio
    page_number = request.GET.get('page', 1)
    properties = service.search_with_pagination(filters, page=page_number, per_page=9)
    
    # Obtener ciudades para el filtro
    cities = service.get_cities()
    
    return render(request, "property_list.html", {
        "properties": properties,
        "cities": cities,
    })


def property_detail(request, pk):
    """
    Detalle de una propiedad.
    Utiliza Service Layer para acceder a la propiedad y calcular estadísticas.
    """
    service = PropertyService()
    
    # Obtener propiedad
    prop = service.get_property_by_id(pk)
    
    # Calcular estadísticas
    stats = service.calculate_property_stats(pk)
    
    # Obtener propiedades similares
    similar = service.get_similar_properties(pk, limit=3)
    
    return render(request, "property_detail.html", {
        "property": prop,
        "stats": stats,
        "similar_properties": similar,
    })


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin para requerir que el usuario sea staff.
    Implementa control de acceso basado en roles.
    """
    def test_func(self):
        return self.request.user.is_staff


class PropertyListView(StaffRequiredMixin, ListView):
    """
    Vista de lista de propiedades para el panel de administración.
    Solo muestra las propiedades del agente autenticado.
    """
    model = Property
    template_name = 'property/property_panel.html'
    context_object_name = 'properties'

    def get_queryset(self):
        """
        Utiliza el servicio para obtener las propiedades del agente.
        DIP: Depende del servicio, no del modelo directamente.
        """
        service = PropertyService()
        return service.get_agent_properties(self.request.user.id)


class PropertyCreateView(StaffRequiredMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'property/property_form.html'
    success_url = reverse_lazy('property_panel')

    def form_valid(self, form):
        
        form.instance.agent = self.request.user
        return super().form_valid(form)


class PropertyUpdateView(StaffRequiredMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'property/property_form.html'
    success_url = reverse_lazy('property_panel')


class PropertyDeleteView(StaffRequiredMixin, DeleteView):
    model = Property
    template_name = 'property/property_confirm_delete.html'
    success_url = reverse_lazy('property_panel')

@login_required
def add_favorite(request, property_id):
    """Añade una propiedad a los favoritos del usuario."""
    property = get_object_or_404(Property, id=property_id)
    request.user.profile.favorites.add(property)
    return redirect(request.META.get('HTTP_REFERER', 'property_list'))

@login_required
def remove_favorite(request, property_id):
    """Quita una propiedad de los favoritos del usuario."""
    property = get_object_or_404(Property, id=property_id)
    request.user.profile.favorites.remove(property)
    return redirect(request.META.get('HTTP_REFERER', 'property_list'))

@login_required
def favorite_list(request):
    """Muestra la lista de propiedades favoritas del usuario."""
    favorites = request.user.profile.favorites.all()
    return render(request, 'property/favorites_list.html', {'favorites': favorites})