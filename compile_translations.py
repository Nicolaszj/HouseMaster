"""
Script para compilar traducciones sin necesitar gettext instalado
Convierte archivos .po a .mo usando polib (Python puro)
"""
import os
import sys
from pathlib import Path

def compile_messages():
    """Compila archivos .po a .mo usando polib"""
    
    try:
        import polib
        print("✅ polib disponible - compilando con Python puro...")
        
        # Buscar archivos .po
        locale_dir = Path(__file__).parent / 'locale'
        
        if not locale_dir.exists():
            print(f"❌ Error: No existe el directorio {locale_dir}")
            return False
        
        compiled_count = 0
        
        for po_file in locale_dir.rglob('*.po'):
            mo_file = po_file.with_suffix('.mo')
            
            try:
                print(f"� Compilando: {po_file.relative_to(locale_dir)}")
                
                # Cargar archivo .po
                po = polib.pofile(str(po_file))
                
                # Guardar como .mo
                po.save_as_mofile(str(mo_file))
                
                print(f"   ✓ Generado: {mo_file.relative_to(locale_dir)}")
                compiled_count += 1
                
            except Exception as e:
                print(f"   ✗ Error al compilar {po_file}: {e}")
        
        if compiled_count > 0:
            print(f"\n✅ {compiled_count} archivo(s) compilado(s) correctamente")
            print("🌐 El sistema i18n ahora debería funcionar")
            print("🔄 Reinicia el servidor Django: python manage.py runserver")
            return True
        else:
            print("⚠️ No se encontraron archivos .po para compilar")
            return False
            
    except ImportError:
        print("❌ Error: polib no está instalado")
        print("💡 Instala con: pip install polib")
        print("   O intenta: python manage.py compilemessages (requiere gettext)")
        return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    success = compile_messages()
    sys.exit(0 if success else 1)
