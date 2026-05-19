# Backend — CafeSys

Sistema web de gestión para cafeterías desarrollado con Django y PostgreSQL. Permite administrar usuarios, productos, pedidos y entregas, con un panel administrativo generado automáticamente por Django Admin.

---

## Tecnologías

| Tecnología | Descripción |
| :--- | :--- |
| Python | Lenguaje de programación |
| Django | Framework backend |
| PostgreSQL | Sistema gestor de base de datos |
| Django REST Framework | API REST |
| Django Admin | Panel administrativo automático |
| python-decouple | Gestión de variables de entorno |
| Git & GitHub | Control de versiones |
| Virtualenv | Gestión de entorno virtual |

---

## Estructura del proyecto

```bash
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
├── venv/
├── .env
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <URL_REPOSITORIO>
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

---

## Configuración

Crear un archivo `.env` en la carpeta `Backend/` con las credenciales de la base de datos:

```env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
```

El archivo `config/settings.py` lee esas variables automáticamente mediante `python-decouple`.

---

## Base de datos

### Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### Crear superusuario

```bash
python manage.py createsuperuser
```

---

## Ejecución

```bash
python manage.py runserver
```

| URL | Descripción |
| :--- | :--- |
| http://127.0.0.1:8000/api/ | API REST |
| http://127.0.0.1:8000/admin/ | Panel de administración |

---

## Modelos implementados

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

## Base de datos

El script SQL con el modelo físico completo se encuentra en:

```
bd/cafeteriadb.sql
```

El DER del sistema se encuentra en:

```
bd/DER-dbdiagram.io.png
```

---

## Autor

Fredy Aragón  
Diego Arce
Gustavo Carrillo
José Rojas
Universidad Nacional de San Agustín de Arequipa