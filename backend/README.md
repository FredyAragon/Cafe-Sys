Backend — CafeSys ☕
Descripción

CafeSys es un sistema web de gestión para cafeterías desarrollado con Django y PostgreSQL.

El backend permite administrar:

Usuarios y roles
Categorías de productos
Productos e ingredientes
Promociones
Pedidos
Ubicaciones de entrega
Vehículos

Además, se implementó Django Admin para generar automáticamente los módulos CRUD del sistema.

Tecnologías utilizadas
Tecnología	Descripción
Python	Lenguaje de programación
Django	Framework backend
PostgreSQL	Sistema gestor de base de datos
Django Admin	Panel administrativo
Git & GitHub	Control de versiones
Virtualenv	Gestión de entorno virtual
Estructura del proyecto
Backend/
│
├── api/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── venv/
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
Instalación del proyecto
1. Clonar el repositorio
git clone <URL_REPOSITORIO>
2. Ingresar al proyecto
cd Backend
3. Crear entorno virtual
python -m venv venv
4. Activar entorno virtual
Windows PowerShell
.\venv\Scripts\Activate
5. Instalar dependencias
pip install -r requirements.txt
Configuración de PostgreSQL

Editar el archivo:

config/settings.py

Configurar la conexión:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cafeteriadb',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
Migraciones
Crear migraciones
python manage.py makemigrations
Aplicar migraciones
python manage.py migrate
Crear superusuario
python manage.py createsuperuser
Ejecutar servidor
python manage.py runserver

Servidor local:

http://127.0.0.1:8000/
Django Admin

Acceso al panel administrativo:

http://127.0.0.1:8000/admin

Desde el panel se pueden administrar automáticamente todos los modelos implementados.

Modelos implementados
Roles
Usuarios
Categorias
Productos
Ingredientes
ProductoIngrediente
Promociones
ProductoPromocion
Departamentos
Provincias
Vehiculos
Ubicaciones
Pedidos
DetallePedidos
Características implementadas

✅ Modelos en Django
✅ Relaciones One-to-Many (FK)
✅ Relaciones Many-to-Many (N:M)
✅ Migraciones automáticas
✅ Django Admin
✅ PostgreSQL
✅ CRUD automático
✅ Restricciones de integridad
✅ DER (Diagrama Entidad Relación)
✅ Entorno virtual
✅ Organización modular del proyecto

Base de datos

La base de datos utilizada es PostgreSQL.

El script SQL se encuentra en:

BD/cafeteriadb.sql

El DER del sistema se encuentra en:

BD/DER-dbdiagram.io.png
Autor

Fredy Aragón
Universidad Nacional de San Agustín