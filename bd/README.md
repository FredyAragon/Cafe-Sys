# Base de Datos — Sistema de Cafetería ☕

## Descripción
Este módulo contiene el diseño y estructura de la base de datos del sistema de cafetería desarrollado con Django y PostgreSQL.

La base de datos permite gestionar:

- Usuarios y roles
- Categorías y productos
- Inventario
- Promociones
- Pedidos y detalles de pedidos
- Ubicaciones de entrega
- Conductores y vehículos
- Entregas
- Reseñas
- Mensajes

---

# Tecnologías utilizadas

- PostgreSQL
- SQL
- Django ORM
- dbdiagram.io

---

# Archivos del módulo BD

| Archivo | Descripción |
|---|---|
| `cafeteriadb.sql` | Script SQL para crear toda la base de datos |
| `DER-dbdiagram.io.png` | Imagen del DER generado en dbdiagram.io |
| `README.md` | Documentación del módulo |
| `.gitignore` | Archivos ignorados por Git |

---

# Estructura de la Base de Datos

La base de datos contiene las siguientes tablas:

1. roles
2. users
3. categories
4. products
5. inventories
6. promotions
7. products_promotions
8. orders
9. order_details
10. locations
11. deliveries
12. drivers
13. vehicles
14. reviews
15. messages

---

# Relaciones principales

- Un usuario pertenece a un rol
- Un producto pertenece a una categoría
- Un pedido pertenece a un usuario
- Un pedido contiene múltiples productos
- Un producto puede tener múltiples ingredientes
- Un producto puede tener múltiples promociones

---

# DER

El diagrama entidad-relación fue generado usando:

https://dbdiagram.io

Archivo relacionado:

- `DER-dbdiagram.io.png`

---

# Cómo usar el script SQL

## 1. Crear la base de datos

```sql
CREATE DATABASE cafeteriadb;