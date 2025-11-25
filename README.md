# Sistema de Inventario Forestal (Evaluación 3)

Este proyecto es una aplicación web desarrollada en **Django** para la gestión de inventario de insumos y repuestos forestales. Permite controlar el stock, registrar movimientos (entradas/salidas) y gestionar usuarios con autenticación segura.

## 📋 Características Principales

*   **Gestión de Insumos**: Crear, listar, editar y eliminar insumos (CRUD).
*   **Control de Movimientos**: Registrar entradas y salidas de stock.
*   **Validación de Stock**: Impide registrar salidas si no hay stock suficiente.
*   **Autenticación**: Login, Logout y Registro de usuarios.
*   **Base de Datos**: Configurado para **MySQL** (Requisito Industrial).
*   **Interfaz Amigable**: Uso de Bootstrap 5 e iconos para una mejor experiencia de usuario.

---

## 🚀 Instalación y Configuración

Sigue estos pasos para levantar el proyecto desde cero.

### 1. Clonar el repositorio y crear entorno virtual

```bash
git clone <url-del-repositorio>
cd ev3backend

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\Activate
# Mac/Linux:
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```
*(Incluye `mysqlclient` y `python-dotenv` necesarios para MySQL)*.

### 3. Configuración de Base de Datos (MySQL)

El proyecto requiere una base de datos MySQL. Se incluye un archivo `.env` en la raíz para configurar tus credenciales.

1.  Crea una base de datos vacía en tu servidor MySQL (ej. `inventario_escolar`).
2.  Edita el archivo `.env` con tus datos:

```ini
MYSQL_DB_NAME=inventario_escolar
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_HOST=localhost
MYSQL_PORT=3306
```

### 4. Inicializar la Base de Datos

Ejecuta las migraciones para crear las tablas en MySQL:

```bash
python manage.py migrate
```

### 5. Poblar con Datos de Prueba (Opcional)

Hemos incluido un comando para cargar datos iniciales (un usuario de prueba, un insumo y un movimiento):

```bash
python manage.py populate_db
```

---

## ▶️ Ejecución

Para iniciar el servidor de desarrollo:

```bash
python manage.py runserver
```

Accede a: **http://127.0.0.1:8000/**

---

## 📖 Guía de Uso

### 1. Inicio de Sesión
Usa las credenciales creadas por el script `populate_db` o crea una cuenta nueva.
*   **Usuario**: `testuser`
*   **Contraseña**: `testpass`
*   *(O Superusuario `admin` / `admin`)*

![Login](file:///C:/Users/the_8/.gemini/antigravity/brain/8a249302-5670-42c7-ba63-4492c46618dd/registro_page_1764029942736.png)
*(La pantalla de login incluye un botón para ver la contraseña y alertas con credenciales de prueba)*.

### 2. Gestión de Insumos
En la página principal verás la lista de insumos. Puedes:
*   **Agregar**: Botón "Nuevo Insumo".
*   **Editar/Eliminar**: Botones de acción en cada fila.
*   **Ver Stock**: El stock se actualiza automáticamente con los movimientos.

### 3. Registrar Movimientos
Ve a la sección de movimientos para registrar entradas o salidas.
*   Selecciona el insumo.
*   Indica la cantidad.
*   El sistema validará si hay suficiente stock para una salida.

---

## 🛠️ Tecnologías

*   **Backend**: Python, Django
*   **Base de Datos**: MySQL / SQLite
*   **Frontend**: HTML5, CSS3, Bootstrap 5
*   **Control de Versiones**: Git

---

## 👨‍💻 Autor
**Jose Camilo Colivoro Uribe**
Desarrollado para la Evaluación 3 de Backend.
