"""
Script para hacer backup de los datos antes de migrar a una base de datos online.
Este script exporta todos los datos en formato JSON usando Django's dumpdata.
"""
import os
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finanzas_perosnales.settings')
django.setup()

from django.core.management import call_command

def hacer_backup():
    """Exporta todos los datos a un archivo JSON"""
    # Crear nombre de archivo con fecha y hora
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archivo_backup = f'backup_datos_{timestamp}.json'
    
    print("🔄 Iniciando backup de datos...")
    print(f"📁 Archivo de backup: {archivo_backup}")
    
    try:
        # Exportar todos los datos
        # Incluye todas las apps del proyecto
        call_command(
            'dumpdata',
            'auth.user',
            'gastos_app',
            'contacto',
            'contenttypes',
            'sessions',
            'admin',
            output=archivo_backup,
            indent=2,
            natural_foreign=True,
            natural_primary=True,
        )
        
        print(f"✅ Backup completado exitosamente!")
        print(f"📦 Archivo guardado en: {os.path.abspath(archivo_backup)}")
        print(f"💾 Tamaño del archivo: {os.path.getsize(archivo_backup)} bytes")
        print("\n⚠️  IMPORTANTE: Guarda este archivo en un lugar seguro antes de migrar.")
        
        return archivo_backup
        
    except Exception as e:
        print(f"❌ Error al hacer backup: {str(e)}")
        return None

if __name__ == '__main__':
    hacer_backup()
