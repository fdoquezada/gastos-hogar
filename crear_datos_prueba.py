# crear_datos_prueba.py
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finanzas_perosnales.settings')
django.setup()

from gastos_app.models import Categoria, InstitucionAhorro, Transaccion, ObjetivoAhorro
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import random

def crear_datos_prueba():
    # Crear o obtener usuario admin
    user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        user.set_password('admin123')
        user.save()
        print("✅ Usuario admin creado (password: admin123)")
    else:
        print("✅ Usuario admin ya existe")

    # Crear categorías básicas
    categorias_ingreso = [
        ('Salario', 'INGRESO', '#10B981'),
        ('Freelance', 'INGRESO', '#059669'),
        ('Inversiones', 'INGRESO', '#047857'),
    ]

    categorias_egreso = [
        ('Alimentación', 'EGRESO', '#EF4444'),
        ('Transporte', 'EGRESO', '#DC2626'),
        ('Vivienda', 'EGRESO', '#B91C1C'),
        ('Entretenimiento', 'EGRESO', '#F59E0B'),
        ('Salud', 'EGRESO', '#D97706'),
        ('Educación', 'EGRESO', '#84CC16'),
        ('Ropa', 'EGRESO', '#65A30D'),
    ]

    categorias_creadas = []
    for nombre, tipo, color in categorias_ingreso + categorias_egreso:
        cat, created = Categoria.objects.get_or_create(
            nombre=nombre,
            tipo=tipo,
            usuario=user,
            defaults={'color': color}
        )
        categorias_creadas.append(cat)
        if created:
            print(f"✅ Categoría creada: {nombre}")

    # Crear instituciones de ahorro
    instituciones = [
        ('Banco ABC', 'Cuenta principal de ahorros'),
        ('Caja XYZ', 'Caja de ahorro local'),
        ('Efectivo', 'Ahorro en efectivo'),
        ('Inversiones', 'Fondos de inversión'),
    ]

    instituciones_creadas = []
    for nombre, descripcion in instituciones:
        inst, created = InstitucionAhorro.objects.get_or_create(
            nombre=nombre,
            usuario=user,
            defaults={'descripcion': descripcion}
        )
        instituciones_creadas.append(inst)
        if created:
            print(f"✅ Institución creada: {nombre}")

    # Crear transacciones de ejemplo para el mes actual
    hoy = timezone.now()
    mes_actual = hoy.replace(day=1)
    
    # Ingresos de ejemplo
    ingresos = [
        (1500.00, 'Salario mensual', 'Salario', 'pago mensual'),
        (300.00, 'Trabajo freelance', 'Freelance', 'proyecto cliente'),
        (150.00, 'Dividendos inversiones', 'Inversiones', 'dividendos'),
    ]

    # Gastos de ejemplo
    gastos = [
        (400.00, 'Supermercado mensual', 'Alimentación', 'compras'),
        (120.00, 'Gasolina del mes', 'Transporte', 'combustible'),
        (800.00, 'Alquiler departamento', 'Vivienda', 'renta'),
        (100.00, 'Cine y restaurante', 'Entretenimiento', 'salida'),
        (50.00, 'Consulta médica', 'Salud', 'doctor'),
        (80.00, 'Libros y cursos', 'Educación', 'estudio'),
        (60.00, 'Ropa nueva', 'Ropa', 'vestimenta'),
    ]

    # Ahorros de ejemplo
    ahorros = [
        (200.00, 'Ahorro mensual banco', 'Banco ABC', 'ahorro programado'),
        (100.00, 'Ahorro efectivo', 'Efectivo', 'reserva'),
    ]

    # Crear transacciones de ingresos
    for monto, descripcion, cat_nombre, glosa in ingresos:
        categoria = next((cat for cat in categorias_creadas if cat.nombre == cat_nombre), None)
        Transaccion.objects.create(
            usuario=user,
            tipo='INGRESO',
            monto=monto,
            descripcion=descripcion,
            glosa=glosa,
            categoria=categoria,
            fecha=mes_actual + timedelta(days=random.randint(1, 28))
        )

    # Crear transacciones de gastos
    for monto, descripcion, cat_nombre, glosa in gastos:
        categoria = next((cat for cat in categorias_creadas if cat.nombre == cat_nombre), None)
        Transaccion.objects.create(
            usuario=user,
            tipo='EGRESO',
            monto=monto,
            descripcion=descripcion,
            glosa=glosa,
            categoria=categoria,
            fecha=mes_actual + timedelta(days=random.randint(1, 28))
        )

    # Crear transacciones de ahorro
    for monto, descripcion, inst_nombre, glosa in ahorros:
        institucion = next((inst for inst in instituciones_creadas if inst.nombre == inst_nombre), None)
        Transaccion.objects.create(
            usuario=user,
            tipo='AHORRO',
            monto=monto,
            descripcion=descripcion,
            glosa=glosa,
            institucion_ahorro=institucion,
            fecha=mes_actual + timedelta(days=random.randint(1, 28))
        )

    # Crear objetivos de ahorro de ejemplo
    objetivos = [
        ('Vacaciones 2025', 'Ahorro para vacaciones en la playa', 2000.00, hoy + timedelta(days=180), 'Banco ABC'),
        ('Nueva Laptop', 'Computadora para trabajo', 1200.00, hoy + timedelta(days=90), 'Efectivo'),
        ('Fondo Emergencia', 'Ahorro para emergencias', 5000.00, hoy + timedelta(days=365), 'Banco ABC'),
    ]

    for nombre, descripcion, monto_objetivo, fecha_objetivo, inst_nombre in objetivos:
        institucion = next((inst for inst in instituciones_creadas if inst.nombre == inst_nombre), None)
        ObjetivoAhorro.objects.create(
            usuario=user,
            nombre=nombre,
            descripcion=descripcion,
            monto_objetivo=monto_objetivo,
            monto_actual=random.randint(100, int(monto_objetivo * 0.7)),
            fecha_objetivo=fecha_objetivo,
            institucion_ahorro=institucion
        )

    print("🎉 ¡Datos de prueba creados exitosamente!")
    print(f"📊 Se crearon:")
    print(f"   - {len(categorias_creadas)} categorías")
    print(f"   - {len(instituciones_creadas)} instituciones")
    print(f"   - {len(ingresos)} transacciones de ingreso")
    print(f"   - {len(gastos)} transacciones de gasto") 
    print(f"   - {len(ahorros)} transacciones de ahorro")
    print(f"   - {len(objetivos)} objetivos de ahorro")
    print("\n🔑 Credenciales para probar:")
    print("   Usuario: admin")
    print("   Password: admin123")

if __name__ == '__main__':
    crear_datos_prueba()