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
| Base de datos | PostgreSQL (Supabase, en desarrollo y producción) |
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
│       ├── models/                   # Definición de tablas (Users, Products, Orders, etc.)
│       ├── admin.py                  # Registro en el panel de administración
│       ├── apps.py                   # Configuración de la app Core
│       ├── create_superuser.py       # Script de creación automática de superusuario
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
├── .env                              # Variables de entorno secretas (NO subir a git)
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

Crea un archivo `.env` en la raíz del backend (usa tus propias credenciales de Supabase; **nunca subas este archivo a git**):

```env
DB_NAME=postgres
DB_USER=<tu_usuario_supabase>
DB_PASSWORD=<tu_password_supabase>
DB_HOST=<tu_host_supabase>
DB_PORT=6543
```

> ⚠️ Si estas credenciales ya se subieron alguna vez a un repositorio público, rota la contraseña desde el dashboard de Supabase inmediatamente, ya que quedan expuestas en el historial de commits aunque se borren después.

### 5. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```bash
python -m apps.core.create_superuser
# Usuario: admin@cafesys.com  |  Contraseña: <definida en el script o variable de entorno>
```

### 7. Levantar el servidor

```bash
python manage.py runserver 0.0.0.0:8081
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

Al iniciar, el contenedor ejecuta automáticamente `migrate --fake-initial`, crea el superusuario mediante `apps.core.create_superuser`, y levanta el servidor de desarrollo de Django. No se despliega ningún contenedor de PostgreSQL local: la conexión se realiza directamente contra Supabase mediante las variables definidas en `backend/.env`.

| URL | Descripción |
| :--- | :--- |
| `http://localhost:8081/api/` | API REST (DRF) |
| `http://localhost:8081/admin/` | Panel administrativo |

**Puertos expuestos:**

| Servicio | Puerto host | Puerto contenedor |
| :--- | :---: | :---: |
| Backend Django | `8081` | `8081` |

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

Cuando el `access` expira (60 minutos), el cliente usa el `refresh` (válido 7 días) en `POST /api/token/refresh/` para obtener uno nuevo sin que el usuario vuelva a iniciar sesión.

**Control de accesos por recurso:**

| Recurso | Lectura (GET) | Escritura (POST/PUT/PATCH/DELETE) |
| :--- | :--- | :--- |
| `Categories`, `Products`, `Promotions` | Pública (`IsAuthenticatedOrReadOnly`) | Cualquier usuario autenticado |
| `Orders` (list/retrieve) | Pública | — |
| `Orders` (crear/actualizar/acciones) | — | Requiere autenticación |
| `Reviews` | Pública (`IsAuthenticatedOrReadOnly`) | Cualquier usuario autenticado |
| `Messages` (crear) | — | Pública (`AllowAny`, formulario de contacto) |
| `Messages` (gestionar) | Requiere autenticación | Requiere autenticación |
| `Users`, `Locations`, `Drivers`, `Vehicles`, `Deliveries`, `OrderDetails` | Requiere autenticación (salvo excepciones puntuales) | Requiere autenticación |

> Nota: a diferencia de un esquema estricto por rol de administrador, la escritura sobre catálogo (productos, categorías, promociones) actualmente solo exige que el usuario esté autenticado, no que tenga un rol administrativo específico.

### Configuración de CORS

Dado que el frontend (Angular) corre en el puerto `8082` y el backend en `8081`, el navegador bloquea las peticiones entre orígenes distintos por defecto. Para resolverlo se configuró **`django-cors-headers`**, que intercepta las *preflight requests* de Angular y valida el origen antes de que Django procese la petición.

**Orígenes permitidos en desarrollo** (`settings.py`):

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://localhost:8082",
    "http://127.0.0.1:8082",
    "https://cafe-sys.vercel.app",
]
```

En producción este valor se actualiza con la URL del frontend desplegado en Vercel.

---

## Endpoints de la API

La API está disponible en `/api/`, registrada mediante un `DefaultRouter` de DRF.

### Autenticación

| Método | Endpoint | Descripción |
| :---: | :--- | :--- |
| POST | `/api/token/` | Obtener par de tokens (access + refresh) |
| POST | `/api/token/refresh/` | Renovar el token de acceso |

### Recursos principales

| Método | Endpoint | Descripción |
| :---: | :--- | :--- |
| GET / POST | `/api/users/` | Listar / registrar usuarios |
| GET / PATCH / DELETE | `/api/users/{id}/` | Detalle, editar, eliminar usuario |
| GET / POST | `/api/categories/` | Listar / crear categorías |
| GET / PATCH / DELETE | `/api/categories/{id}/` | Detalle, editar, eliminar categoría |
| GET / POST | `/api/products/` | Listar / crear productos |
| GET / PATCH / DELETE | `/api/products/{id}/` | Detalle, editar, eliminar producto |
| GET / POST | `/api/promotions/` | Listar / crear promociones |
| GET / PATCH / DELETE | `/api/promotions/{id}/` | Detalle, editar, eliminar promoción |
| GET / POST | `/api/products-promotions/` | Relación producto–promoción |
| GET / POST | `/api/locations/` | Listar / crear direcciones de entrega |
| GET / POST | `/api/orders/` | Listar / crear pedidos |
| GET / PUT | `/api/orders/{id}/` | Detalle, actualizar pedido |
| POST | `/api/orders/{id}/advance_status/` | Avanzar el estado del pedido |
| POST | `/api/orders/{id}/cancel/` | Cancelar pedido propio en estado pendiente |
| POST | `/api/orders/{id}/archive/` | Archivar pedido |
| GET / POST | `/api/order-details/` | Listar / crear líneas de pedido |
| GET / POST | `/api/drivers/` | Listar / crear conductores |
| GET / POST | `/api/vehicles/` | Listar / crear vehículos |
| GET / POST | `/api/deliveries/` | Listar / crear entregas |
| GET / POST | `/api/reviews/` | Listar / crear reseñas |
| GET / POST | `/api/messages/` | Listar mensajes / enviar mensaje de contacto (público) |

> El panel navegable de DRF está disponible en cada endpoint desde el navegador.

---

## Modelos del sistema

| Modelo | Descripción |
| :--- | :--- |
| `Users` | Usuarios registrados en el sistema, con campo `role` (Customer, Admin, Employee, Driver) |
| `Categories` | Categorías de productos del catálogo |
| `Products` | Productos disponibles en la cafetería |
| `Promotions` | Promociones y descuentos configurables |
| `ProductsPromotions` | Relación N:M entre productos y promociones |
| `Locations` | Direcciones de entrega registradas por usuario |
| `Orders` | Pedidos realizados por los usuarios |
| `OrderDetails` | Detalle de productos por pedido |
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

> Configura las variables de entorno en Render con los datos de conexión de Supabase; nunca las incluyas en el repositorio.

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