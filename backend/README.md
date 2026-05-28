# ☕ CafeSys — Backend

Sistema web de gestión para cafeterías desarrollado con **Django** y **SupaBase**. Permite administrar usuarios, productos, pedidos y entregas, con un panel administrativo generado automáticamente por Django Admin.

---

## 🧰 Tecnologías

| Tecnología | Descripción |
| :--- | :--- |
| Python | Lenguaje de programación |
| Django | Framework backend |
| SupaBase | Sistema gestor de base de datos |
| Django REST Framework | API REST |
| Django Admin | Panel administrativo automático |
| python-decouple | Gestión de variables de entorno |
| Docker & Docker Compose | Contenedorización del proyecto |
| Git & GitHub | Control de versiones |
| Virtualenv | Gestión de entorno virtual |

---

## 📁 Estructura del proyecto

```
Backend/
├── api/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── .env
├── .gitignore
├── create_superuser.py
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalación local

### 1. Clonar el repositorio

```bash
git clone https://github.com/FredyAragon/Cafe-Sys.git

cd Backend
```


### 2. Crear y activar el entorno virtual

```bash
python -m venv venv

# Windows PowerShell
.\venv\Scripts\Activate

# Linux / macOS
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones y crear superusuario

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Ejecutar el servidor

```bash
python manage.py runserver
```

| URL | Descripción |
| :--- | :--- |
| http://127.0.0.1:8000/api/ | API REST |
| http://127.0.0.1:8000/admin/ | Panel de administración |

---

## 🐳 Docker

### Levantar con Docker Compose

```bash
docker-compose up --build
```

Las migraciones y el superusuario se crean automáticamente al iniciar el contenedor.

| URL | Descripción |
| :--- | :--- |
| http://localhost:8081/api/ | API REST |
| http://localhost:8081/admin/ | Panel de administración |

**Credenciales del admin:**

| Campo | Valor |
| :--- | :--- |
| Usuario | `admin` |
| Contraseña | `admin` |

---

## 🌐 Endpoints principales

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| GET | `/api/productos/` | Listar productos |
| POST | `/api/productos/` | Crear producto |
| GET | `/api/pedidos/` | Listar pedidos |
| POST | `/api/pedidos/` | Crear pedido |
| GET | `/api/usuarios/` | Listar usuarios |

---

## 🗄️ Modelos implementados

| Modelo | Descripción |
| :--- | :--- |
| Roles | Roles del sistema (admin, cliente) |
| Users | Usuarios del sistema |
| Categories | Categorías de productos |
| Products | Productos del catálogo |
| Inventory | Stock de productos |
| Promotions | Promociones y descuentos |
| Products_Promotions | Productos con promoción (N:M) |
| Vehicles | Vehículos de reparto |
| Drivers | Conductores |
| Locations | Direcciones de entrega del cliente |
| Orders | Pedidos |
| Orders_Products | Detalle de pedidos (N:M) |
| Deliveries | Envíos |
| Messages | Mensajes de contacto |
| Reviews | Reseñas de productos |

---

## 📊 Base de datos

El script SQL con el modelo físico completo:

```
bd/cafeteriadb.sql
```

El Diagrama Entidad-Relación del sistema:

```
bd/DER-dbdiagram.io.png
```

---

## 👥 Equipo

| Nombre | Rol |
| :--- | :--- |
| Fredy José Aragón Carpio | Desarrollador Backend |
| Diego Marcelo Arce Coaquira | Desarrollador y Diseñador Frontend |
| Gustavo Alonso Carrillo Villalta | Desarrollador de Base de Datos |
| José Manuel Rojas Bravo | Desarrollador Full-Stack |

**Universidad Nacional de San Agustín de Arequipa**
Escuela Profesional de Ingeniería de Sistemas
