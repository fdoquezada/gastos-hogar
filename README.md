# 💰 Gastos del Hogar

Sistema de gestión de finanzas personales desarrollado con Django. Permite a los usuarios llevar un control completo de sus ingresos, gastos, ahorros y presupuestos mensuales.

## 📋 Características Principales

### 💵 Gestión de Transacciones
- **Ingresos y Egresos**: Registra todos tus movimientos financieros
- **Ahorros**: Controla tus ahorros en distintas instituciones
- **Traspasos**: Movimientos entre meses o categorías
- **Recurrencia**: Configura transacciones automáticas (diarias, semanales, mensuales, anuales)

### 📊 Categorías Personalizadas
- Categorías personalizadas para ingresos y egresos
- Asignación de colores para visualización
- Organización por tipo de transacción

### 🎯 Presupuestos Mensuales
- Establece presupuestos por categoría
- Seguimiento en tiempo real del uso del presupuesto
- Alertas cuando te acercas o excedes tus límites
- Visualización del porcentaje de uso y monto restante

### 🏦 Instituciones de Ahorro
- Gestiona múltiples cuentas e instituciones
- Asocia ahorros con instituciones específicas
- Control centralizado de todos tus ahorros

### 🎯 Objetivos de Ahorro
- Define objetivos con fecha y monto específico
- Seguimiento del progreso con visualización de porcentaje
- Alertas de fechas límite
- Asociación con instituciones de ahorro

### 🔔 Sistema de Alertas
- Alertas por límites de presupuesto alcanzados
- Recordatorios de objetivos de ahorro
- Notificaciones de pagos programados
- Marcado de alertas como leídas

### 📈 Dashboard
- Vista general de tus finanzas
- Resumen de ingresos, gastos y ahorros
- Gráficos y estadísticas visuales
- Análisis por categorías

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 4.2.18
- **Base de Datos**: PostgreSQL (configurable)
- **Frontend**: HTML, CSS, JavaScript
- **Bootstrap**: Para diseño responsivo
- **Python**: 3.x

### Principales Dependencias
- `django` - Framework web
- `psycopg2` - Adaptador PostgreSQL
- `django-crispy-forms` - Formularios estilizados
- `python-decouple` - Gestión de variables de entorno
- `gunicorn` - Servidor WSGI para producción
- `whitenoise` - Servir archivos estáticos

## 📦 Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip o pipenv
- PostgreSQL (opcional, puede usar SQLite para desarrollo)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd gastoshogar
```

2. **Crear y activar entorno virtual**
```bash
python -m venv entorno
# En Windows:
entorno\Scripts\activate
# En Linux/Mac:
source entorno/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
Crea un archivo `.env` en la raíz del proyecto:
```env
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

5. **Realizar migraciones**
```bash
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

8. **Acceder a la aplicación**
Abre tu navegador en `http://127.0.0.1:8000`

## 🚀 Datos de Prueba

El proyecto incluye un script para crear datos de prueba:

```bash
python crear_datos_prueba.py
```

Este script creará:
- Usuario admin con las credenciales:
  - **Usuario**: `admin`
  - **Contraseña**: `admin123`
- Categorías predefinidas (ingresos y egresos)
- Instituciones de ahorro de ejemplo
- Transacciones de ejemplo para el mes actual
- Objetivos de ahorro de muestra

## 📁 Estructura del Proyecto

```
gastoshogar/
├── finanzas_perosnales/      # Configuración del proyecto Django
│   ├── settings.py           # Configuraciones
│   ├── urls.py              # URLs principales
│   └── wsgi.py              # Configuración WSGI
├── gastos_app/              # Aplicación principal de gastos
│   ├── models.py            # Modelos de datos
│   ├── views.py             # Vistas
│   ├── forms.py             # Formularios
│   ├── urls.py              # URLs de la app
│   └── templates/           # Plantillas HTML
│       └── gastos_app/      # Templates de la app
├── contacto/                # Aplicación de contacto
├── static/                  # Archivos estáticos (CSS, JS, imágenes)
├── templates/               # Templates base
├── manage.py                # Script de gestión Django
├── requirements.txt         # Dependencias del proyecto
├── crear_datos_prueba.py   # Script para datos de prueba
└── README.md               # Este archivo
```

## 🎨 Modelos Principales

### Categoria
- Gestiona categorías de ingresos y egresos
- Asociada a usuarios
- Color personalizable

### Transaccion
- Tipos: INGRESO, EGRESO, AHORRO, TRASPASO
- Asociada a categorías y/o instituciones de ahorro
- Soporte para transacciones recurrentes

### PresupuestoMensual
- Presupuestos por categoría y mes
- Cálculo automático de gastos
- Métricas de uso y estado

### InstitucionAhorro
- Gestiona diferentes instituciones financieras
- Asociada a transacciones de ahorro

### ObjetivoAhorro
- Metas de ahorro con fecha límite
- Seguimiento de progreso
- Alertas automáticas

### Alerta
- Sistema de notificaciones
- Tipos: PRESUPUESTO, OBJETIVO, PAGO
- Control de lectura

## 🔒 Seguridad

- Autenticación de usuarios con Django
- Validación de formularios
- Protección CSRF habilitada
- Variables sensibles en archivo `.env`
- Validación de permisos por usuario

## 🚀 Despliegue en Producción

1. Configurar variables de entorno en producción
2. Cambiar `DEBUG = False`
3. Configurar `ALLOWED_HOSTS` apropiadamente
4. Usar un servidor web como Nginx + Gunicorn
5. Configurar base de datos PostgreSQL
6. Ejecutar `python manage.py collectstatic`

## 📝 Licencia

Ver archivo `LICENSE` para más detalles.

## 👨‍💻 Contribución

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Contacto

Para consultas o soporte, utiliza el formulario de contacto en la aplicación o abre un issue en el repositorio.

---

**Desarrollado con ❤️ usando Django**