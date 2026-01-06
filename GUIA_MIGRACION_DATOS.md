# 📋 Guía de Migración de Datos a Base de Datos Online

## ❓ ¿Pierdes los datos al cambiar a una base de datos online?

**¡NO!** Si sigues estos pasos correctamente, **NO perderás ningún dato**.

## 📝 Pasos para Migrar de Forma Segura

### Paso 1: Hacer Backup de tus Datos Actuales

Antes de cambiar nada, **siempre** haz un backup:

```bash
python backup_datos.py
```

Esto creará un archivo `backup_datos_YYYYMMDD_HHMMSS.json` con todos tus datos.

### Paso 2: Obtener la URL de tu Base de Datos Online

Dependiendo del proveedor de base de datos online que uses, obtendrás una URL similar a:

**PostgreSQL (ElephantSQL, Render, Heroku, Railway, etc.):**
```
postgresql://usuario:contraseña@host:puerto/nombre_bd
```

**MySQL/MariaDB:**
```
mysql://usuario:contraseña@host:puerto/nombre_bd
```

### Paso 3: Configurar la Nueva Base de Datos

#### Opción A: Usando archivo `.env` (Recomendado)

1. Crea o edita el archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_bd
```

2. Tu `settings.py` ya está configurado para leer esta variable automáticamente.

#### Opción B: Variable de entorno del sistema

En Windows (PowerShell):
```powershell
$env:DATABASE_URL="postgresql://usuario:contraseña@host:puerto/nombre_bd"
```

En Linux/Mac:
```bash
export DATABASE_URL="postgresql://usuario:contraseña@host:puerto/nombre_bd"
```

### Paso 4: Crear las Tablas en la Nueva Base de Datos

Ejecuta las migraciones para crear la estructura de la base de datos:

```bash
python manage.py migrate
```

### Paso 5: Restaurar tus Datos

Restaura todos tus datos desde el backup:

```bash
python restaurar_datos.py backup_datos_YYYYMMDD_HHMMSS.json
```

### Paso 6: Verificar que Todo Funcione

1. Inicia el servidor:
```bash
python manage.py runserver
```

2. Accede a tu aplicación y verifica que:
   - Puedes iniciar sesión
   - Tus transacciones están ahí
   - Tus categorías están ahí
   - Tus presupuestos están ahí
   - Todo funciona correctamente

## 🔄 Migración Paso a Paso (Resumen)

```bash
# 1. Backup (con la base de datos antigua configurada)
python backup_datos.py

# 2. Configurar nueva base de datos (editar .env o variable de entorno)
# DATABASE_URL=nueva_url_aqui

# 3. Crear estructura en nueva base de datos
python manage.py migrate

# 4. Restaurar datos
python restaurar_datos.py backup_datos_YYYYMMDD_HHMMSS.json

# 5. Verificar
python manage.py runserver
```

## ⚠️ Importante

1. **Nunca elimines tu base de datos antigua** hasta que hayas verificado que todo funciona correctamente en la nueva.

2. **Guarda el archivo de backup** en un lugar seguro (nube, disco externo, etc.).

3. **Prueba primero en un entorno de desarrollo** si es posible.

4. Si algo sale mal, puedes volver a la base de datos antigua simplemente cambiando la `DATABASE_URL` de vuelta.

## 🆘 Si Algo Sale Mal

### Error: "Table already exists"
- La base de datos ya tiene datos. Opcionalmente puedes limpiarla primero:
```bash
python manage.py flush
```
Y luego restaurar el backup.

### Error: "Connection refused" o similar
- Verifica que la URL de la base de datos sea correcta
- Verifica que tu IP esté autorizada en el proveedor de base de datos online
- Verifica que el firewall permita conexiones a ese puerto

### Error al cargar datos
- Asegúrate de haber ejecutado `migrate` primero
- Verifica que el archivo de backup no esté corrupto
- Revisa los mensajes de error para más detalles

## 📞 ¿Necesitas Ayuda?

Si tienes problemas, verifica:
1. Los logs de errores de Django
2. Los logs de tu proveedor de base de datos online
3. Que todas las dependencias estén instaladas (`pip install -r requirements.txt`)

## ✅ Checklist Final

- [ x] Backup realizado y guardado en lugar seguro
- [ ] Nueva base de datos configurada y accesible
- [ ] Migraciones ejecutadas en nueva base de datos
- [ ] Datos restaurados desde el backup
- [ ] Aplicación probada y funcionando correctamente
- [ ] Base de datos antigua guardada como respaldo adicional
