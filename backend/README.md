# ☕ CafeSys — Backend

> Sistema de gestión para cafeterías construido con **Django REST Framework** y **PostgreSQL**.  
> Expone una API REST completa para gestionar usuarios, productos, pedidos y entregas,  
> con panel administrativo integrado vía Django Admin.

---

## Stack tecnológico

| Capa | Tecnología |
| :--- | :--- |
| Lenguaje | Python 3.10+ |
| Framework | Django + Django REST Framework |
| Base de datos | PostgreSQL 17 (local) / Supabase (producción) |
| Autenticación | Simple JWT + Django Admin |
| Variables de entorno | python-decouple |
| Contenedorización | Docker & Docker Compose |
| Control de versiones | Git & GitHub |
| Entorno virtual | venv |

---

## Estructura del proyecto

```
backend/
│
├── apps/
│   └── core/                         # Aplicación principal del sistema
│       ├── migrations/               # Historial de migraciones a Supabase
│       ├── models/                   # Definición de tablas (Ej. Product)
│       ├── admin.py                  # Registro en el panel de administración
│       ├── apps.py                   # Configuración de la app Core
│       ├── serializers.py            # Conversión de modelos a JSON
│       ├── urls.py                   # Enrutamiento de la API Core
│       └── views.py                  # Lógica de controladores / endpoints
│
├── cafesys/                          # Configuración global de Django
│   ├── settings.py                   # Ajustes generales y CORS
│   ├── urls.py                       # Enrutador raíz del proyecto
│   ├── asgi.py
│   └── wsgi.py
│
├── venv/                             # Entorno virtual local (Python)
├── .env                              # Variables de entorno secretas
├── .gitignore
├── Dockerfile                        # Configuración del contenedor backend
├── manage.py                         # Gestor de comandos de Django
├── README.md
└── requirements.txt                  # Dependencias (django-cors-headers, etc.)
```

---

## Instalación local

### 1. Clonar el repositorio

```bash
git clone https://github.com/FredyAragon/Cafe-Sys.git
cd Cafe-Sys/backend
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate

# Linux / macOS
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del backend:

```env
DB_NAME=postgres
DB_USER=postgres.uybtqkpxkcivbzpgcsrm
DB_PASSWORD=s5GkqPPwdb8nfDuB
DB_HOST=aws-1-us-west-1.pooler.supabase.com
DB_PORT=6543
```

### 5. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```bash
python create_superuser.py
# Usuario: admin@cafesys.com  |  Contraseña: admin1234
```

### 7. Levantar el servidor

```bash
python manage.py runserver
```

| URL | Descripción |
| :--- | :--- |
| `http://127.0.0.1:8081/api/` | API REST (DRF) |
| `http://127.0.0.1:8081/admin/` | Panel administrativo |

---

## Docker

### Levantar con Docker Compose

Desde la raíz del proyecto (donde está el `docker-compose.yml`):

```bash
docker-compose up --build
```

Las migraciones y el superusuario se crean automáticamente al iniciar el contenedor.

| URL | Descripción |
| :--- | :--- |
| `http://localhost:8081/api/` | API REST (DRF) |
| `http://localhost:8081/admin/` | Panel administrativo |

**Credenciales del admin:**

| Campo | Valor |
| :--- | :--- |
| Usuario | `admin@cafesys.com` |
| Contraseña | `admin1234` |

**Puertos expuestos:**

| Servicio | Puerto host | Puerto contenedor |
| :--- | :---: | :---: |
| Backend Django | `8081` | `8081` |
| PostgreSQL | `8085` | `5432` |

---

## Seguridad y arquitectura

El sistema implementa una arquitectura desacoplada (*Decoupled Architecture*) donde el frontend (Angular, puerto `8082`) y el backend (Django REST Framework, puerto `8081`) se comunican de forma segura mediante políticas CORS y autenticación basada en tokens JWT.

### Autenticación con JWT

Para proteger los endpoints sensibles se utiliza **djangorestframework-simplejwt**.

**Flujo de autenticación:**

```
POST /api/token/
{ "email": "...", "password": "..." }
        ↓
{ "access": "<token de corta duración>", "refresh": "<token de renovación>" }
```

El token `access` se incluye en cada petición protegida mediante el header:

```
Authorization: Bearer <access_token>
```

Cuando el `access` expira, el cliente usa el `refresh` en `POST /api/token/refresh/` para obtener uno nuevo sin que el usuario vuelva a iniciar sesión.

**Control de accesos por rol (`IsAdminOrReadOnly`):**

Se implementó una clase de permiso personalizada que aplica la siguiente lógica:

| Método HTTP | Quién puede acceder |
| :---: | :--- |
| `GET`, `HEAD`, `OPTIONS` | Cualquiera (incluye anónimos) |
| `POST`, `PUT`, `PATCH`, `DELETE` | Solo usuarios con `is_staff = True` |

```python
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )
```

Esta clase se aplica en los ViewSets de `Categories`, `Products`, `Promotions` y `ProductsPromotions`. Los endpoints de `Orders`, `Inventories`, `Deliveries`, `Messages` y similares requieren únicamente `IsAuthenticated` (cualquier usuario logueado). `Reviews` usa `IsAuthenticatedOrReadOnly` para que cualquier cliente registrado pueda publicar una reseña.

### Configuración de CORS

Dado que el frontend (Angular) corre en el puerto `8082` y el backend en `8081`, el navegador bloquea las peticiones entre orígenes distintos por defecto. Para resolverlo se configuró **`django-cors-headers`**, que intercepta las *preflight requests* de Angular y valida el origen antes de que Django procese la petición.

**Orígenes permitidos en desarrollo** (`settings.py`):

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8082",
    "http://127.0.0.1:8082",
]
```

En producción este valor se actualiza con la URL del frontend desplegado en Render.

---

## Endpoints de la API

La API está disponible en `/api/`. Las operaciones de escritura requieren un token JWT de administrador (ver sección de seguridad).

### Autenticación

| Método | Endpoint | Descripción |
| :---: | :--- | :--- |
| POST | `/api/token/` | Obtener par de tokens (access + refresh) |
| POST | `/api/token/refresh/` | Renovar el token de acceso |

### Recursos principales

| Método | Endpoint | Descripción |
| :---: | :--- | :--- |
| GET / POST | `/api/roles/` | Listar / crear roles |
| GET / PUT / DELETE | `/api/roles/{id}/` | Detalle, editar, eliminar rol |
| GET / POST | `/api/users/` | Listar / crear usuarios |
| GET / PUT / DELETE | `/api/users/{id}/` | Detalle, editar, eliminar usuario |
| GET / POST | `/api/categories/` | Listar / crear categorías |
| GET / PUT / DELETE | `/api/categories/{id}/` | Detalle, editar, eliminar categoría |
| GET / POST | `/api/products/` | Listar / crear productos |
| GET / PUT / DELETE | `/api/products/{id}/` | Detalle, editar, eliminar producto |
| GET / POST | `/api/orders/` | Listar / crear pedidos |
| GET / PUT / DELETE | `/api/orders/{id}/` | Detalle, editar, eliminar pedido |
| GET / POST | `/api/promotions/` | Listar / crear promociones |
| GET / PUT / DELETE | `/api/promotions/{id}/` | Detalle, editar, eliminar promoción |
| GET / POST | `/api/deliveries/` | Listar / crear entregas |
| GET / PUT / DELETE | `/api/deliveries/{id}/` | Detalle, editar, eliminar entrega |

> El panel navegable de DRF está disponible en cada endpoint desde el navegador.

---

## Modelos del sistema

| Modelo | Descripción |
| :--- | :--- |
| `Roles` | Roles del sistema (admin, cliente, etc.) |
| `Users` | Usuarios registrados en el sistema |
| `Categories` | Categorías de productos del catálogo |
| `Products` | Productos disponibles en la cafetería |
| `Inventories` | Control de stock por producto |
| `Promotions` | Promociones y descuentos configurables |
| `ProductsPromotions` | Relación N:M entre productos y promociones |
| `Locations` | Direcciones de entrega registradas por usuario |
| `Orders` | Pedidos realizados por los usuarios |
| `OrderDetails` | Detalle de productos por pedido (N:M) |
| `Deliveries` | Envíos asignados a conductores |
| `Drivers` | Conductores disponibles para entregas |
| `Vehicles` | Vehículos asociados a los conductores |
| `Reviews` | Reseñas de productos por usuario |
| `Messages` | Mensajes de contacto o soporte |

---

## Despliegue en producción

El backend está configurado para desplegarse en **Render** conectado a **Supabase** como base de datos en la nube.

| Recurso | URL |
| :--- | :--- |
| API en producción | `https://cafesys-backend.onrender.com/api/` |
| Panel admin | `https://cafesys-backend.onrender.com/admin/` |
| Base de datos | Supabase — proyecto `https://supabase.com/dashboard/project/uybtqkpxkcivbzpgcsrm` |

> Configura las variables de entorno en Render con los datos de conexión de Supabase.

---

## Equipo

| Nombre | Rol |
| :--- | :--- |
| Fredy José Aragón Carpio | Desarrollador Backend |
| Diego Marcelo Arce Coaquira | Desarrollador y Diseñador Frontend |
| Gustavo Alonso Carrillo Villalta | Desarrollador de Base de Datos |
| José Manuel Bravo Rojas | Desarrollador Full-Stack |

**Universidad Nacional de San Agustín de Arequipa**  
Escuela Profesional de Ingeniería de Sistemas — DAW 2026-A