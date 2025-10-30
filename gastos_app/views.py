from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q, Count
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from .models import ObjetivoAhorro
from .forms import ObjetivoAhorroForm
import json
from django.http import HttpResponse, JsonResponse

from .models import *
from .forms import *

def registro_usuario(request):
    """Vista para el formulario de registro de nuevos usuarios."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'¡Cuenta creada exitosamente para {user.username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
        
    return render(request, 'registration/registro.html', {'form': form})

def inicio(request):
    """Vista de inicio que redirige al dashboard o login según el estado de autenticación"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'gastos_app/inicio.html')

# ==================== DASHBOARD PRINCIPAL ====================
@login_required
def dashboard(request):
    """Vista principal del dashboard con estadísticas"""
    hoy = timezone.now()
    mes_actual = hoy.replace(day=1)
    mes_siguiente = (mes_actual + timedelta(days=32)).replace(day=1)
    
    # Transacciones del mes actual
    transacciones_mes = Transaccion.objects.filter(
        usuario=request.user,
        fecha__gte=mes_actual,
        fecha__lt=mes_siguiente
    )
    
    # Estadísticas básicas
    total_ingresos = transacciones_mes.filter(tipo='INGRESO').aggregate(
        Sum('monto'))['monto__sum'] or 0
    total_egresos = transacciones_mes.filter(tipo='EGRESO').aggregate(
        Sum('monto'))['monto__sum'] or 0
    total_ahorros = transacciones_mes.filter(tipo='AHORRO').aggregate(
        Sum('monto'))['monto__sum'] or 0
    # Verificar y crear alertas automáticamente


    # Ahorro por institución
    ahorro_por_institucion = Transaccion.objects.filter(
        usuario=request.user,
        tipo='AHORRO',
        fecha__gte=mes_actual,
        fecha__lt=mes_siguiente
    ).values('institucion_ahorro__nombre').annotate(
        total=Sum('monto')
    ).order_by('-total')
    
    # Si no hay resultados, mostrar instituciones disponibles
    if not ahorro_por_institucion:
        instituciones = InstitucionAhorro.objects.filter(usuario=request.user)
        ahorro_por_institucion = [{
            'institucion_ahorro__nombre': inst.nombre,
            'total': 0
        } for inst in instituciones]
    
    ultimas_transacciones = Transaccion.objects.filter(
        usuario=request.user
    ).order_by('-fecha')[:10]
    
    gastos_por_categoria = Transaccion.objects.filter(
        usuario=request.user,
        tipo='EGRESO',
        fecha__gte=mes_actual,
        fecha__lt=mes_siguiente
    ).values('categoria__nombre', 'categoria__color').annotate(
        total=Sum('monto')
    ).order_by('-total')
    
    objetivos = ObjetivoAhorro.objects.filter(
        usuario=request.user, 
        completado=False
    )[:5]
    
    alertas_count = Alerta.objects.filter(
        usuario=request.user, 
        leida=False
    ).count()
    
    context = {
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'total_ahorros': total_ahorros,
        'balance_actual': total_ingresos - total_egresos - total_ahorros,
        'ahorro_por_institucion': list(ahorro_por_institucion),
        'ultimas_transacciones': ultimas_transacciones,
        'gastos_por_categoria': list(gastos_por_categoria),
        'objetivos': objetivos,
        'alertas_count': alertas_count,
        'mes_actual': mes_actual.strftime('%B %Y'),
    }
    
    return render(request, 'gastos_app/dashboard.html', context)

# ==================== GESTIÓN DE TRANSACCIONES ====================
@login_required
def agregar_transaccion(request):
    """Vista para agregar nueva transacción"""
    if request.method == 'POST':
        form = TransaccionForm(request.POST, usuario=request.user)
        if form.is_valid():
            transaccion = form.save(commit=False)
            transaccion.usuario = request.user
            transaccion.save()
            messages.success(request, '✅ Transacción agregada correctamente')
            return redirect('dashboard')
    else:
        form = TransaccionForm(usuario=request.user)
    
    return render(request, 'gastos_app/agregar_transaccion.html', {'form': form})

@login_required
def listar_transacciones(request):
    """Vista para listar y filtrar transacciones"""
    transacciones = Transaccion.objects.filter(usuario=request.user).order_by('-fecha')
    
    # Filtros
    tipo_filter = request.GET.get('tipo')
    categoria_filter = request.GET.get('categoria')
    glosa_filter = request.GET.get('glosa')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    if tipo_filter:
        transacciones = transacciones.filter(tipo=tipo_filter)
    if categoria_filter:
        transacciones = transacciones.filter(categoria_id=categoria_filter)
    if glosa_filter:
        transacciones = transacciones.filter(glosa__icontains=glosa_filter)
    if fecha_desde:
        transacciones = transacciones.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        transacciones = transacciones.filter(fecha__lte=fecha_hasta)
    
    categorias = Categoria.objects.filter(usuario=request.user)
    
    context = {
        'transacciones': transacciones,
        'categorias': categorias,
    }
    
    return render(request, 'gastos_app/listar_transacciones.html', context)

@login_required
def editar_transaccion(request, id):
    """Vista para editar una transacción existente"""
    transaccion = get_object_or_404(Transaccion, id=id, usuario=request.user)
    
    if request.method == 'POST':
        form = TransaccionForm(request.POST, instance=transaccion, usuario=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Transacción actualizada correctamente')
            return redirect('listar_transacciones')
    else:
        form = TransaccionForm(instance=transaccion, usuario=request.user)
    
    return render(request, 'gastos_app/editar_transaccion.html', {'form': form})

@login_required
def eliminar_transaccion(request, id):
    """Vista para eliminar una transacción"""
    transaccion = get_object_or_404(Transaccion, id=id, usuario=request.user)
    
    if request.method == 'POST':
        transaccion.delete()
        messages.success(request, '✅ Transacción eliminada correctamente')
        return redirect('listar_transacciones')
    
    return render(request, 'gastos_app/eliminar_transaccion.html', {'transaccion': transaccion})

# ==================== TRASPASOS ENTRE MESES ====================
@login_required
def traspaso_mes(request):
    """Vista para realizar traspasos de saldo entre meses"""
    if request.method == 'POST':
        form = TraspasoForm(request.POST, usuario=request.user)
        if form.is_valid():
            # Crear transacción de egreso del mes actual
            egreso = Transaccion(
                usuario=request.user,
                tipo='TRASPASO',
                monto=form.cleaned_data['monto'],
                descripcion=f"Traspaso al mes {form.cleaned_data['mes_destino'].strftime('%Y-%m')}",
                glosa=form.cleaned_data['glosa'],
                es_traspaso=True,
                fecha=timezone.now()
            )
            egreso.save()
            
            # Crear transacción de ingreso para el mes destino
            ingreso = Transaccion(
                usuario=request.user,
                tipo='TRASPASO',
                monto=form.cleaned_data['monto'],
                descripcion=f"Traspaso del mes {timezone.now().strftime('%Y-%m')}",
                glosa=form.cleaned_data['glosa'],
                es_traspaso=True,
                fecha=form.cleaned_data['mes_destino']
            )
            ingreso.save()
            
            # Actualizar el traspaso origen con el destino
            egreso.traspaso_destino = ingreso
            egreso.save()
            
            messages.success(request, '✅ Traspaso realizado correctamente')
            return redirect('dashboard')
    else:
        form = TraspasoForm(usuario=request.user)
    
    return render(request, 'gastos_app/traspaso_mes.html', {'form': form})

# ==================== PRESUPUESTOS ====================
# ==================== PRESUPUESTOS ====================
@login_required
def gestionar_presupuestos(request):
    """Vista para gestionar presupuestos mensuales"""
    hoy = timezone.now()
    mes_actual = hoy.replace(day=1)
    
    if request.method == 'POST':
        form = PresupuestoForm(request.POST, usuario=request.user)
        if form.is_valid():
            presupuesto = form.save(commit=False)
            presupuesto.usuario = request.user
            presupuesto.mes = mes_actual  # ← IMPORTANTE: Asignar el mes actual
            presupuesto.save()
            
            # ✅ DETECTAR SI ES PETICIÓN AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': '✅ Presupuesto agregado correctamente'
                })
            else:
                messages.success(request, '✅ Presupuesto agregado correctamente')
                return redirect('presupuestos')
        else:
            # ✅ MANEJAR ERRORES DE VALIDACIÓN EN AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': '❌ Error en el formulario',
                    'errors': form.errors
                })
    else:
        form = PresupuestoForm(usuario=request.user)
    
    # Obtener presupuestos del mes actual
    presupuestos = PresupuestoMensual.objects.filter(
        usuario=request.user,
        mes=mes_actual
    )
    
    # ==================== NUEVAS ESTADÍSTICAS ====================
    
    # Calcular totales
    total_presupuestado = sum(p.monto_presupuestado for p in presupuestos)
    total_gastado = sum(p.monto_gastado() for p in presupuestos)
    total_restante = total_presupuestado - total_gastado
    
    # Categorizar presupuestos por estado
    presupuestos_buen_estado = [p for p in presupuestos if p.porcentaje_uso() <= 80]
    presupuestos_alerta = [p for p in presupuestos if 80 < p.porcentaje_uso() <= 100]
    presupuestos_excedidos = [p for p in presupuestos if p.porcentaje_uso() > 100]
    
    # Encontrar categorías sin presupuesto (solo categorías de EGRESO)
    categorias_con_presupuesto_ids = presupuestos.values_list('categoria_id', flat=True)
    categorias_sin_presupuesto = Categoria.objects.filter(
        usuario=request.user, 
        tipo='EGRESO'
    ).exclude(id__in=categorias_con_presupuesto_ids)
    
    # Calcular promedio de uso
    if presupuestos:
        promedio_uso = sum(p.porcentaje_uso() for p in presupuestos) / len(presupuestos)
    else:
        promedio_uso = 0
    
    # ==================== CONTEXT ACTUALIZADO ====================
    
    context = {
        'form': form,
        'presupuestos': presupuestos,
        'mes_actual': mes_actual.strftime('%B %Y'),
        # Nuevas variables para el template mejorado
        'total_presupuestado': total_presupuestado,
        'total_gastado': total_gastado,
        'total_restante': total_restante,
        'presupuestos_buen_estado': presupuestos_buen_estado,
        'presupuestos_alerta': presupuestos_alerta,
        'presupuestos_excedidos': presupuestos_excedidos,
        'categorias_sin_presupuesto': categorias_sin_presupuesto,
        'promedio_uso': promedio_uso,
    }
    
    # ✅ SI ES AJAX Y GET, PODRÍAS MANEJARLO DE FORMA DIFERENTE
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        return JsonResponse({'success': True, 'message': 'Datos cargados'})
    
    return render(request, 'gastos_app/presupuestos.html', context)

# ==================== AGREGAR ESTA FUNCIÓN QUE FALTA ====================
@login_required
def editar_presupuesto(request, presupuesto_id):
    """Vista para editar un presupuesto existente - ESTA ES LA QUE FALTA"""
    presupuesto = get_object_or_404(PresupuestoMensual, id=presupuesto_id, usuario=request.user)
    
    if request.method == 'POST':
        form = PresupuestoForm(request.POST, instance=presupuesto, usuario=request.user)
        if form.is_valid():
            form.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'message': '✅ Presupuesto actualizado correctamente'
                })
            else:
                messages.success(request, '✅ Presupuesto actualizado correctamente')
                return redirect('presupuestos')
    else:
        form = PresupuestoForm(instance=presupuesto, usuario=request.user)
    
    # Si es AJAX, retornar solo el formulario
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'gastos_app/partials/form_editar_presupuesto.html', {
            'form': form,
            'presupuesto': presupuesto
        })
    
    return render(request, 'gastos_app/editar_presupuesto.html', {
        'form': form,
        'presupuesto': presupuesto
    })

@login_required
def detalles_presupuesto(request, presupuesto_id):
    presupuesto = get_object_or_404(PresupuestoMensual, id=presupuesto_id, usuario=request.user)
    
    # Obtener transacciones recientes de esta categoría
    transacciones = Transaccion.objects.filter(
        usuario=request.user,
        categoria=presupuesto.categoria,
        fecha__year=presupuesto.mes.year,
        fecha__month=presupuesto.mes.month,
        tipo='EGRESO'
    ).order_by('-fecha')[:10]
    
    data = {
        'success': True,
        'presupuesto': {
            'monto_presupuestado': float(presupuesto.monto_presupuestado),
            'monto_gastado': float(presupuesto.monto_gastado()),
            'monto_restante': float(presupuesto.monto_restante),
            'monto_excedido': float(presupuesto.monto_excedido),
            'porcentaje_uso': round(presupuesto.porcentaje_uso(), 1)
        },
        'transacciones': [
            {
                'fecha': trans.fecha.strftime('%d/%m/%Y'),
                'descripcion': trans.descripcion,
                'monto': float(trans.monto)
            }
            for trans in transacciones
        ]
    }
    
    return JsonResponse(data)

@login_required
def eliminar_presupuesto(request, presupuesto_id):
    presupuesto = get_object_or_404(PresupuestoMensual, id=presupuesto_id, usuario=request.user)
    
    if request.method == 'POST':
        presupuesto.delete()
        return JsonResponse({'success': True, 'message': '✅ Presupuesto eliminado correctamente'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})
# ==================== OBJETIVOS DE AHORRO ====================
@login_required
def objetivos_ahorro(request):
    """Vista principal para gestionar objetivos de ahorro"""
    objetivos = ObjetivoAhorro.objects.filter(usuario=request.user)
    
    if request.method == 'POST':
        form = ObjetivoAhorroForm(request.POST, usuario=request.user)
        if form.is_valid():
            objetivo = form.save(commit=False)
            objetivo.usuario = request.user
            objetivo.save()
            messages.success(request, '✅ Objetivo de ahorro creado correctamente')
            return redirect('objetivos')
    else:
        form = ObjetivoAhorroForm(usuario=request.user)
    
    context = {
        'objetivos': objetivos,
        'form': form,
    }
    return render(request, 'gastos_app/objetivos.html', context)

# VISTA FALTANTE - AGREGAR OBJETIVO
@login_required
def agregar_objetivo(request):
    """Vista para agregar nuevo objetivo de ahorro"""
    if request.method == 'POST':
        form = ObjetivoAhorroForm(request.POST, usuario=request.user)
        if form.is_valid():
            objetivo = form.save(commit=False)
            objetivo.usuario = request.user
            objetivo.save()
            messages.success(request, '✅ Objetivo de ahorro creado correctamente')
            return redirect('objetivos')
    else:
        form = ObjetivoAhorroForm(usuario=request.user)
    
    return render(request, 'gastos_app/agregar_objetivo.html', {'form': form})

@login_required
def agregar_ahorro_objetivo(request, id):
    """Vista para agregar monto a un objetivo de ahorro"""
    objetivo = get_object_or_404(ObjetivoAhorro, id=id, usuario=request.user)
    
    if request.method == 'POST':
        monto_agregar = request.POST.get('monto_agregar')
        try:
            monto_agregar = Decimal(monto_agregar)
            if monto_agregar > 0:
                objetivo.monto_actual += monto_agregar
                
                # Marcar como completado si alcanza el objetivo
                if objetivo.monto_actual >= objetivo.monto_objetivo:
                    objetivo.monto_actual = objetivo.monto_objetivo
                    objetivo.completado = True
                
                objetivo.save()
                messages.success(request, f'✅ Se agregaron ${monto_agregar} al objetivo "{objetivo.nombre}"')
            else:
                messages.error(request, '❌ El monto debe ser mayor a cero')
        except (ValueError, InvalidOperation):
            messages.error(request, '❌ Monto inválido')
        
        return redirect('objetivos')
    
    return render(request, 'gastos_app/agregar_ahorro.html', {'objetivo': objetivo})

@login_required
def editar_objetivo(request, id):
    """Vista para editar un objetivo de ahorro"""
    objetivo = get_object_or_404(ObjetivoAhorro, id=id, usuario=request.user)
    
    if request.method == 'POST':
        form = ObjetivoAhorroForm(request.POST, instance=objetivo, usuario=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Objetivo actualizado correctamente')
            return redirect('objetivos')
    else:
        form = ObjetivoAhorroForm(instance=objetivo, usuario=request.user)
    
    return render(request, 'gastos_app/editar_objetivo.html', {
        'form': form,
        'objetivo': objetivo
    })

@login_required
def eliminar_objetivo(request, id):
    """Vista para eliminar un objetivo de ahorro"""
    objetivo = get_object_or_404(ObjetivoAhorro, id=id, usuario=request.user)
    
    if request.method == 'POST':
        objetivo.delete()
        messages.success(request, '✅ Objetivo eliminado correctamente')
        return redirect('objetivos')
    
    return render(request, 'gastos_app/eliminar_objetivo.html', {'objetivo': objetivo})

# ==================== ALERTAS ====================
@login_required
def alertas(request):
    """Vista para ver y gestionar alertas"""
    alertas = Alerta.objects.filter(usuario=request.user, leida=False).order_by('-fecha_creacion')
    
    if request.method == 'POST' and 'marcar_leidas' in request.POST:
        alertas.update(leida=True)
        messages.success(request, '✅ Alertas marcadas como leídas')
        return redirect('alertas')
    
    context = {
        'alertas': alertas,
    }
    return render(request, 'gastos_app/alertas.html', context)

# ==================== CATEGORÍAS ====================
@login_required
def categorias(request):
    """Vista para listar categorías del usuario"""
    categorias_usuario = Categoria.objects.filter(usuario=request.user)
    return render(request, 'gastos_app/categorias.html', {
        'categorias': categorias_usuario
    })

@login_required
def agregar_categoria(request):
    """Vista para agregar nueva categoría"""
    if request.method == 'POST':
        form = CategoriaForm(request.POST, usuario=request.user)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = request.user
            categoria.save()
            messages.success(request, '✅ Categoría agregada correctamente')
            return redirect('categorias')
    else:
        form = CategoriaForm(usuario=request.user)
    
    return render(request, 'gastos_app/agregar_categoria.html', {'form': form})

@login_required
def editar_categoria(request, categoria_id):
    """Vista para editar categoría existente"""
    categoria = get_object_or_404(Categoria, id=categoria_id, usuario=request.user)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria, usuario=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Categoría actualizada correctamente')
            return redirect('categorias')
    else:
        form = CategoriaForm(instance=categoria, usuario=request.user)
    
    return render(request, 'gastos_app/editar_categoria.html', {'form': form})

@login_required
def eliminar_categoria(request, categoria_id):
    """Vista para eliminar categoría"""
    categoria = get_object_or_404(Categoria, id=categoria_id, usuario=request.user)
    
    if request.method == 'POST':
        # Verificar que no hay transacciones usando esta categoría
        transacciones_con_categoria = Transaccion.objects.filter(categoria=categoria, usuario=request.user)
        
        if transacciones_con_categoria.exists():
            messages.error(request, '❌ No puedes eliminar esta categoría porque tiene transacciones asociadas')
        else:
            categoria.delete()
            messages.success(request, '✅ Categoría eliminada correctamente')
        
        return redirect('categorias')
    
    return render(request, 'gastos_app/eliminar_categoria.html', {'categoria': categoria})

# ==================== INSTITUCIONES DE AHORRO ====================
@login_required
def instituciones_ahorro(request):
    """Vista para listar instituciones de ahorro del usuario"""
    instituciones = InstitucionAhorro.objects.filter(usuario=request.user)
    return render(request, 'gastos_app/instituciones.html', {'instituciones': instituciones})

# VISTAS FALTANTES - INSTITUCIONES
@login_required
def agregar_institucion(request):
    """Vista para agregar nueva institución de ahorro"""
    if request.method == 'POST':
        form = InstitucionAhorroForm(request.POST, usuario=request.user)
        if form.is_valid():
            institucion = form.save(commit=False)
            institucion.usuario = request.user
            institucion.save()
            messages.success(request, '✅ Institución agregada correctamente')
            return redirect('instituciones_ahorro')
    else:
        form = InstitucionAhorroForm(usuario=request.user)
    
    return render(request, 'gastos_app/agregar_institucion.html', {'form': form})

@login_required
def editar_institucion(request, institucion_id):
    """Vista para editar institución existente"""
    institucion = get_object_or_404(InstitucionAhorro, id=institucion_id, usuario=request.user)
    
    if request.method == 'POST':
        form = InstitucionAhorroForm(request.POST, instance=institucion, usuario=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Institución actualizada correctamente')
            return redirect('instituciones_ahorro')
    else:
        form = InstitucionAhorroForm(instance=institucion, usuario=request.user)
    
    return render(request, 'gastos_app/editar_institucion.html', {'form': form})

@login_required
def eliminar_institucion(request, institucion_id):
    """Vista para eliminar institución"""
    institucion = get_object_or_404(InstitucionAhorro, id=institucion_id, usuario=request.user)
    
    if request.method == 'POST':
        # Verificar que no hay transacciones usando esta institución
        transacciones_con_institucion = Transaccion.objects.filter(institucion_ahorro=institucion, usuario=request.user)
        
        if transacciones_con_institucion.exists():
            messages.error(request, '❌ No puedes eliminar esta institución porque tiene transacciones asociadas')
        else:
            institucion.delete()
            messages.success(request, '✅ Institución eliminada correctamente')
        
        return redirect('instituciones_ahorro')
    
    return render(request, 'gastos_app/eliminar_institucion.html', {'institucion': institucion})

# ==================== APIS INTERNAS ====================
@login_required
def api_estadisticas(request):
    """API para obtener estadísticas en formato JSON"""
    hoy = timezone.now()
    mes_actual = hoy.replace(day=1)
    
    transacciones_mes = Transaccion.objects.filter(
        usuario=request.user,
        fecha__gte=mes_actual
    )
    
    data = {
        'total_ingresos': float(transacciones_mes.filter(tipo='INGRESO').aggregate(Sum('monto'))['monto__sum'] or 0),
        'total_egresos': float(transacciones_mes.filter(tipo='EGRESO').aggregate(Sum('monto'))['monto__sum'] or 0),
        'total_ahorros': float(transacciones_mes.filter(tipo='AHORRO').aggregate(Sum('monto'))['monto__sum'] or 0),
    }
    
    return JsonResponse(data)

# ==================== VISTAS PARA MODALES ====================
@login_required
def agregar_categoria_modal(request):
    """Vista para el formulario de categoría en modal"""
    if request.method == 'POST':
        form = CategoriaForm(request.POST, usuario=request.user)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = request.user
            categoria.save()
            
            # Verificar si es una petición AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'message': '✅ Categoría agregada correctamente'
                })
            else:
                # Redirigir de vuelta a agregar transacción
                return redirect('agregar_transaccion')
                
    else:
        form = CategoriaForm(usuario=request.user)
    
    return render(request, 'gastos_app/partials/form_categoria.html', {'form': form})

@login_required
def agregar_institucion_modal(request):
    """Vista para el formulario de institución en modal"""
    if request.method == 'POST':
        form = InstitucionAhorroForm(request.POST, usuario=request.user)
        if form.is_valid():
            institucion = form.save(commit=False)
            institucion.usuario = request.user
            institucion.save()
            
            # Verificar si es una petición AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'message': '✅ Institución agregada correctamente'
                })
            else:
                # Redirigir de vuelta a agregar transacción
                return redirect('agregar_transaccion')
                
    else:
        form = InstitucionAhorroForm(usuario=request.user)
    
    return render(request, 'gastos_app/partials/form_institucion.html', {'form': form})