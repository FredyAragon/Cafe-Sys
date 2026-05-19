# ☕ Cafe-Sys

Sistema web de gestión para cafeterías desarrollado como proyecto académico utilizando tecnologías web modernas.

Cafe-Sys permite administrar productos, usuarios, pedidos, promociones, inventario y entregas mediante una arquitectura modular compuesta por backend, frontend y base de datos.

---

# 📌 Objetivo del proyecto

El objetivo de Cafe-Sys es digitalizar y optimizar los procesos de una cafetería, permitiendo:

- Gestión de productos y categorías
- Administración de usuarios y roles
- Control de inventario
- Gestión de pedidos
- Administración de promociones
- Seguimiento de entregas
- Gestión de vehículos y conductores
- Registro de reseñas y mensajes

---

# 🧰 Tecnologías utilizadas

| Área | Tecnologías |
| :--- | :--- |
| Backend | Django, Django REST Framework |
| Base de Datos | PostgreSQL |
| Frontend | HTML, CSS, JavaScript |
| Control de versiones | Git & GitHub |
| Modelado BD | dbdiagram.io |

---

# 📁 Estructura general del proyecto

```bash
Cafe-Sys/
│
├── Backend/
│   ├── api/
│   ├── config/
│   ├── requirements.txt
│   └── README.md
│
├── BD/
│   ├── cafeteriadb.sql
│   ├── DER-dbdiagram.io.png
│   └── README.md
│
├── Frontend/
│
├── Informes/
│
├── .gitignore
└── README.md
```

---

# 🧩 Módulos principales

## Backend

Contiene la lógica del sistema desarrollada con Django y Django REST Framework.

Incluye:

- API REST
- Modelos ORM
- Serializers
- Views
- URLs
- Django Admin

---

## Base de Datos

Contiene el diseño lógico y físico de la base de datos del sistema.

Incluye:

- Script SQL completo
- DER del sistema
- Restricciones y relaciones

---

## Frontend

Contiene la interfaz gráfica del sistema para clientes y administradores.

---

# 📦 Funcionalidades del sistema

- Gestión de usuarios y roles
- Administración de productos
- Gestión de inventario
- Registro de pedidos
- Control de promociones
- Gestión de entregas
- Administración de vehículos y conductores
- Sistema de reseñas
- Mensajería y contacto

---

# 🗄️ Entidades principales

El sistema trabaja con las siguientes tablas principales:

1. Roles  
2. Users  
3. Categories  
4. Products  
5. Inventories  
6. Promotions  
7. ProductsPromotions  
8. Orders  
9. OrderDetails  
10. Locations  
11. Deliveries  
12. Drivers  
13. Vehicles  
14. Reviews  
15. Messages  

---

# 👨‍💻 Integrantes

- Fredy Aragón
- Diego Arce
- Gustavo Carrillo
- José Rojas

---

# 🏫 Universidad

Universidad Nacional de San Agustín de Arequipa

Curso: **Desarrollo de Aplicaciones Web — Proyecto Grupal**