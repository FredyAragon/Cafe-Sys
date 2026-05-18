# ☕ Cafe-Sys — Backend (Django + PostgreSQL)

Sistema backend del proyecto Cafe-Sys, desarrollado con Django REST Framework y conectado a una base de datos PostgreSQL ya existente.

Este backend expone una API REST para la gestión de productos, usuarios, pedidos, inventario, promociones y demás componentes del sistema.

---

## 🚀 Repositorio

Rama de trabajo del backend: **Cafe-Sys** (`rama: Gustavo`)

Para clonar directamente:

```bash
git clone https://github.com/FredyAragon/Cafe-Sys.git
git checkout Gustavo
```

---

## 🧰 Tecnologías utilizadas

- Python 3.13
- Django
- Django REST Framework
- PostgreSQL
- ORM de Django
- Django Admin

---

## 📁 Estructura principal

```
Cafe-Sys/
└── backend/
     ├── api/
     ├── config/
     ├── manage.py
     ├── requirements.txt
     └── .gitignore
```

---

## ⚙️ Requisitos previos

Antes de levantar el proyecto debes tener instalado:

- Python 3.10+
- PostgreSQL en ejecución
- La base de datos del proyecto ya creada y poblada

> ⚠️ **Importante:** Django no crea la base de datos. Django se conecta a la base de datos PostgreSQL ya existente.

---

## ▶️ Cómo levantar el proyecto

Desde la raíz del repositorio:

```bash
git clone https://github.com/FredyAragon/Cafe-Sys.git
cd Cafe-Sys/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver 8081
```

El servidor quedará activo en:

```
http://localhost:8081
```

---

## 🔐 Acceso al panel de administración (Django Admin)

Crear superusuario:

```bash
python manage.py createsuperuser
```

Luego ingresar a:

```
http://localhost:8081/admin
```

Desde aquí se pueden:

- Crear productos
- Registrar usuarios
- Gestionar pedidos
- Editar promociones
- Administrar inventario

Todo desde interfaz gráfica.