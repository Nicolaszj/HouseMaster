from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Property
from django.core.paginator import Paginator
from django.db.models import Q


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

    # ciudades únicas para el filtro select
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