# ☕ Cafe-Sys — Base de Datos (PostgreSQL + Supabase)

Sistema de base de datos del proyecto Cafe-Sys, diseñado con un modelo
relacional en PostgreSQL e implementado en Supabase como plataforma BaaS.

Este módulo contiene el modelo lógico DER, los scripts SQL de creación
e inserción de datos para la gestión de productos, usuarios, pedidos,
promociones y demás componentes del sistema.

---

## 🚀 Repositorio

Rama de trabajo de la base de datos: **Cafe-Sys** (`rama: Gustavo`)

Para clonar directamente:

```bash
git clone https://github.com/FredyAragon/Cafe-Sys.git
git checkout Gustavo
```

---

## 🧰 Tecnologías utilizadas

- PostgreSQL
- Supabase (BaaS — Backend as a Service)
- SQL estándar
- dbdiagram.io (modelado DER)

---

## 📁 Estructura principal
Cafe-Sys/
└── bd/
├── bd.sql
├── .gitignore
└── README.md

---

## ⚙️ Requisitos previos

Antes de ejecutar los scripts debes tener:

- Cuenta activa en Supabase
- Proyecto creado en el dashboard de Supabase
- Acceso al editor SQL de Supabase

> ⚠️ **Importante:** Los scripts deben ejecutarse en orden. Las tablas
> con claves foráneas dependen de que sus tablas referenciadas existan
> previamente.

---

## ▶️ Cómo ejecutar la base de datos

Desde el dashboard de Supabase:
supabase.com/dashboard → Tu proyecto → SQL Editor → New Query

Pegar y ejecutar el contenido de:
bd/bd.sql

Verificar las tablas creadas:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

---

## 🗂️ Tablas del sistema

| # | Tabla | Descripción |
|---|---|---|
| 1 | roles | Roles de usuario (admin, cliente) |
| 2 | usuarios | Clientes y administradores |
| 3 | categorias | Categorías de productos |
| 4 | productos | Productos del menú |
| 5 | ingredientes | Ingredientes de cada producto |
| 6 | promociones | Descuentos y ofertas |
| 7 | departamentos | Ubigeo — departamentos |
| 8 | provincias | Ubigeo — provincias |
| 9 | vehiculos | Vehículos de reparto |
| 10 | ubicaciones | Direcciones de entrega |
| 11 | pedidos | Pedidos realizados |
| 12 | detalle_pedidos | Detalle de cada pedido |
| 13 | producto_ingrediente | Relación N:M producto-ingrediente |
| 14 | producto_promocion | Relación N:M producto-promoción |

---

## 🔍 Acceso al panel de Supabase

Ingresar a:
https://supabase.com/dashboard

Desde aquí se pueden:

- Visualizar las tablas creadas
- Consultar y editar registros
- Ejecutar queries SQL
- Gestionar relaciones y claves foráneas
- Exportar la base de datos

Todo desde interfaz gráfica.