from django.contrib import admin
from .models import (
    Categoria, 
    InstitucionAhorro, 
    Transaccion, 
    PresupuestoMensual, 
    ObjetivoAhorro, 
    Alerta
)

# Registro básico para modelos simples
admin.site.register(Categoria)
admin.site.register(InstitucionAhorro)

# Configuración avanzada para modelos más complejos
@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'monto', 'descripcion', 'fecha', 'categoria', 'es_recurrente')
    list_filter = ('tipo', 'es_recurrente', 'es_traspaso', 'fecha', 'usuario')
    search_fields = ('descripcion', 'glosa', 'usuario__username')
    date_hierarchy = 'fecha'
    ordering = ('-fecha',)
    list_per_page = 25

@admin.register(PresupuestoMensual)
class PresupuestoMensualAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'mes', 'categoria', 'monto_presupuestado', 'monto_gastado', 'porcentaje_uso')
    list_filter = ('mes', 'usuario', 'categoria')
    search_fields = ('usuario__username', 'categoria__nombre')
    ordering = ('-mes', 'usuario')
    list_per_page = 25

    def monto_gastado(self, obj):
        return obj.monto_gastado()
    monto_gastado.short_description = 'Monto Gastado'

    def porcentaje_uso(self, obj):
        return f"{obj.porcentaje_uso():.1f}%"
    porcentaje_uso.short_description = 'Porcentaje Usado'

@admin.register(ObjetivoAhorro)
class ObjetivoAhorroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'monto_actual', 'monto_objetivo', 'porcentaje_completado', 'dias_restantes', 'completado')
    list_filter = ('completado', 'fecha_objetivo', 'usuario', 'institucion_ahorro')
    search_fields = ('nombre', 'descripcion', 'usuario__username')
    ordering = ('-fecha_objetivo',)
    list_per_page = 25

    def porcentaje_completado(self, obj):
        return f"{obj.porcentaje_completado():.1f}%"
    porcentaje_completado.short_description = 'Completado'

    def dias_restantes(self, obj):
        return obj.dias_restantes()
    dias_restantes.short_description = 'Días Restantes'

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'tipo', 'leida', 'fecha_creacion')
    list_filter = ('tipo', 'leida', 'fecha_creacion', 'usuario')
    search_fields = ('titulo', 'mensaje', 'usuario__username')
    ordering = ('-fecha_creacion',)
    list_per_page = 25
    actions = ['marcar_como_leidas']

    def marcar_como_leidas(self, request, queryset):
        queryset.update(leida=True)
    marcar_como_leidas.short_description = 'Marcar alertas seleccionadas como leídas'