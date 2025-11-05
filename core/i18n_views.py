"""
Vista de verificación del sistema i18n
Muestra el estado de las traducciones y permite probar el cambio de idioma
"""
from django.shortcuts import render
from django.utils.translation import get_language, gettext as _
from django.conf import settings
import os

def i18n_test(request):
    """Vista para verificar el sistema i18n"""
    
    current_lang = get_language()
    
    # Verificar archivos .mo compilados
    locale_path = settings.LOCALE_PATHS[0] if settings.LOCALE_PATHS else None
    mo_files = {}
    
    if locale_path:
        for lang_code, lang_name in settings.LANGUAGES:
            mo_path = os.path.join(locale_path, lang_code, 'LC_MESSAGES', 'django.mo')
            po_path = os.path.join(locale_path, lang_code, 'LC_MESSAGES', 'django.po')
            mo_files[lang_code] = {
                'name': lang_name,
                'mo_exists': os.path.exists(mo_path),
                'po_exists': os.path.exists(po_path),
                'mo_path': mo_path,
                'po_path': po_path,
            }
    
    # Palabras de prueba
    test_words = [
        _('Inicio'),
        _('Propiedades'),
        _('Contacto'),
        _('Favoritos'),
        _('Venta'),
        _('Arriendo'),
    ]
    
    context = {
        'current_language': current_lang,
        'languages': settings.LANGUAGES,
        'mo_files': mo_files,
        'test_words': test_words,
        'i18n_enabled': settings.USE_I18N,
        'locale_path': locale_path,
    }
    
    return render(request, 'i18n_test.html', context)
