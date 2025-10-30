from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum # Añadimos Sum aquí para la función monto_gastado

# ====================
# MODELOS DE GASTOS APP
# ====================

class Categoria(models.Model):
    TIPO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('EGRESO', 'Egreso'),
    ]
    
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=7, default='#3B82F6')
    
    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

class InstitucionAhorro(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('EGRESO', 'Egreso'),
        ('AHORRO', 'Ahorro'),
        ('TRASPASO', 'Traspaso'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    glosa = models.CharField(max_length=200, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    institucion_ahorro = models.ForeignKey(InstitucionAhorro, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField(default=timezone.now)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Para transacciones recurrentes
    es_recurrente = models.BooleanField(default=False)
    frecuencia_recurrencia = models.CharField(max_length=20, choices=[
        ('DIARIA', 'Diaria'),
        ('SEMANAL', 'Semanal'),
        ('MENSUAL', 'Mensual'),
        ('ANUAL', 'Anual')
    ], blank=True, null=True)
    
    # Para traspasos entre meses
    es_traspaso = models.BooleanField(default=False)
    traspaso_destino = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.fecha} - {self.tipo} - ${self.monto} - {self.descripcion}"

# --- PresupuestoMensual (Versión Final y Única) ---

class PresupuestoMensual(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mes = models.DateField()  # Primer día del mes
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    monto_presupuestado = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ['usuario', 'mes', 'categoria']
    
    def monto_gastado(self):
        # Esta implementación de 'monto_gastado' estaba en ambas versiones
        gastos = Transaccion.objects.filter(
            usuario=self.usuario,
            categoria=self.categoria,
            fecha__year=self.mes.year,
            fecha__month=self.mes.month,
            tipo='EGRESO'
        ).aggregate(Sum('monto'))['monto__sum'] or 0
        return gastos
    
    def porcentaje_uso(self):
        # Esta implementación de 'porcentaje_uso' estaba en ambas versiones
        if self.monto_presupuestado == 0:
            return 0
        return (self.monto_gastado() / self.monto_presupuestado) * 100
    
    # ==================== NUEVOS MÉTODOS PARA EL TEMPLATE MEJORADO (Añadidos de la segunda definición) ====================
    
    @property
    def monto_restante(self):
        """Calcula el monto que queda disponible en el presupuesto"""
        return self.monto_presupuestado - self.monto_gastado()
    
    @property
    def monto_excedido(self):
        """Calcula cuánto se ha excedido del presupuesto (si aplica)"""
        gastado = self.monto_gastado()
        if gastado > self.monto_presupuestado:
            return gastado - self.monto_presupuestado
        return 0
    
    def estado(self):
        """Devuelve el estado del presupuesto para usar en templates"""
        porcentaje = self.porcentaje_uso()
        if porcentaje > 100:
            return 'excedido'
        elif porcentaje > 80:
            return 'alerta'
        else:
            return 'buen_estado'
    
    def __str__(self):
        return f"{self.categoria.nombre} - {self.mes.strftime('%Y-%m')}" 

# --- Modelos ObjetivoAhorro y Alerta ---

class ObjetivoAhorro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    monto_objetivo = models.DecimalField(max_digits=10, decimal_places=2)
    monto_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_objetivo = models.DateField()
    institucion_ahorro = models.ForeignKey(InstitucionAhorro, on_delete=models.CASCADE)
    completado = models.BooleanField(default=False)
    
    def porcentaje_completado(self):
        if self.monto_objetivo == 0:
            return 0
        return (self.monto_actual / self.monto_objetivo) * 100
    
    def dias_restantes(self):
        return (self.fecha_objetivo - timezone.now().date()).days
    
    def __str__(self):
        return self.nombre

class Alerta(models.Model):
    TIPO_ALERTA = [
        ('PRESUPUESTO', 'Límite de presupuesto'),
        ('OBJETIVO', 'Objetivo de ahorro'),
        ('PAGO', 'Recordatorio de pago'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_ALERTA)
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    relacion_id = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.tipo} - {self.titulo}"