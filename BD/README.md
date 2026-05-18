# Base de Datos — Sistema de Cafetería ☕

## Descripción
Este módulo contiene el diseño y estructura de la base de datos del sistema de cafetería desarrollado con Django y PostgreSQL.

La base de datos permite gestionar:

- Usuarios y roles
- Categorías de productos
- Productos e ingredientes
- Promociones
- Pedidos y detalle de pedidos
- Ubicaciones de entrega
- Departamentos y provincias
- Vehículos

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
2. usuarios
3. categorias
4. productos
5. ingredientes
6. producto_ingrediente
7. promociones
8. producto_promocion
9. departamentos
10. provincias
11. vehiculos
12. ubicaciones
13. pedidos
14. detalle_pedidos

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