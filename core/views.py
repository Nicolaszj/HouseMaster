from django.shortcuts import render

def home(request):
    """
    Vista para la página de inicio.
    
    Renderiza la plantilla home.html.
    """
    return render(request, 'core/home.html')
