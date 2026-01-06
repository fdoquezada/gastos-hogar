"""
Script para restaurar los datos desde un backup JSON después de migrar a una base de datos online.
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finanzas_perosnales.settings')
django.setup()

from django.core.management import call_command

def restaurar_backup(archivo_backup):
    """Restaura los datos desde un archivo JSON de backup"""
    
    if not os.path.exists(archivo_backup):
        print(f"❌ Error: El archivo {archivo_backup} no existe.")
        return False
    
    print("🔄 Iniciando restauración de datos...")
    print(f"📁 Archivo de backup: {archivo_backup}")
    
    try:
        # Primero limpiar la base de datos (OPCIONAL - solo si quieres empezar desde cero)
        # Descomenta las siguientes líneas solo si quieres limpiar primero:
        # print("⚠️  Limpiando base de datos existente...")
        # call_command('flush', '--noinput')
        
        # Cargar los datos desde el backup
        call_command('loaddata', archivo_backup, verbosity=2)
        
        print(f"✅ Datos restaurados exitosamente!")
        print("🎉 Tu aplicación ahora tiene todos los datos de vuelta.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al restaurar backup: {str(e)}")
        print("\n💡 Consejos:")
        print("   - Verifica que la base de datos esté configurada correctamente")
        print("   - Asegúrate de haber ejecutado las migraciones: python manage.py migrate")
        print("   - Verifica que el archivo de backup sea válido")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("📖 Uso: python restaurar_datos.py <archivo_backup.json>")
        print("\nEjemplo:")
        print("   python restaurar_datos.py backup_datos_20250115_143022.json")
        sys.exit(1)
    
    archivo = sys.argv[1]
    restaurar_backup(archivo)
