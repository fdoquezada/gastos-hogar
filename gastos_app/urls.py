from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    
    # Authentication
    path('registro/', views.registro_usuario, name='registro'),
    
    # Dashboard y transacciones
    path('dashboard/', views.dashboard, name='dashboard'),  # ⬅️ CORREGIDO: "dashboard" no "dashoard"
    path('agregar/', views.agregar_transaccion, name='agregar_transaccion'),
    path('transacciones/', views.listar_transacciones, name='listar_transacciones'),
    path('editar/<int:id>/', views.editar_transaccion, name='editar_transaccion'),
    path('eliminar/<int:id>/', views.eliminar_transaccion, name='eliminar_transaccion'),
    path('traspaso/', views.traspaso_mes, name='traspaso_mes'),
    
    # Gestión financiera
    # URLs para presupuestos
    path('presupuestos/', views.gestionar_presupuestos, name='presupuestos'),
    path('presupuestos/detalles/<int:presupuesto_id>/', views.detalles_presupuesto, name='detalles_presupuesto'),
    path('presupuestos/editar/<int:presupuesto_id>/', views.editar_presupuesto, name='editar_presupuesto'),
    path('presupuestos/eliminar/<int:presupuesto_id>/', views.eliminar_presupuesto, name='eliminar_presupuesto'),
    path('objetivos/', views.objetivos_ahorro, name='objetivos'),
    
    # URLs para funcionalidades de objetivos
    path('objetivos/agregar/', views.agregar_objetivo, name='agregar_objetivo'),  # ⬅️ AGREGADO
    path('objetivos/agregar_ahorro/<int:id>/', views.agregar_ahorro_objetivo, name='agregar_ahorro_objetivo'),
    path('objetivos/editar/<int:id>/', views.editar_objetivo, name='editar_objetivo'),
    path('objetivos/eliminar/<int:id>/', views.eliminar_objetivo, name='eliminar_objetivo'),
    
    # URLs para categorías
    path('categorias/', views.categorias, name='categorias'),
    path('categorias/agregar/', views.agregar_categoria, name='agregar_categoria'),
    path('categorias/editar/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),
    
    # URLs para instituciones
    path('instituciones/', views.instituciones_ahorro, name='instituciones_ahorro'),
    path('instituciones/agregar/', views.agregar_institucion, name='agregar_institucion'),  # ⬅️ AGREGADO
    path('instituciones/editar/<int:institucion_id>/', views.editar_institucion, name='editar_institucion'),  # ⬅️ AGREGADO
    path('instituciones/eliminar/<int:institucion_id>/', views.eliminar_institucion, name='eliminar_institucion'),  # ⬅️ AGREGADO
    
    # Alertas
    path('alertas/', views.alertas, name='alertas'),
    
    # APIs
    path('api/estadisticas/', views.api_estadisticas, name='api_estadisticas'),

    # URLs para modales
path('categorias/agregar/modal/', views.agregar_categoria_modal, name='agregar_categoria_modal'),
path('instituciones/agregar/modal/', views.agregar_institucion_modal, name='agregar_institucion_modal'),
]