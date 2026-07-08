# Base de Datos — Sistema de Cafetería ☕ (Café-Sys)

##  Descripción
Este módulo contiene el diseño, scripts, datos iniciales y la estructura de la base de datos relacional para el sistema de cafetería, mapeado directamente desde el backend de **Django ORM** y persistido en **PostgreSQL / Supabase**.

El diseño permite gestionar el flujo completo del negocio:
* **Usuarios y Autenticación:** Clientes, administradores y roles del sistema.
* **Catálogo e Inventario:** Categorías, productos y promociones dinámicas.
* **Ventas:** Pedidos y detalles de facturación (`order_details`).
* **Logística de Entregas:** Ubicaciones (`locations`), conductores (`drivers`), vehículos y estados de envío.
* **Feedback y Comunicación:** Sistema de reseñas (`reviews`) y mensajería interna (`messages`).

---

##  Tecnologías Utilizadas
* **PostgreSQL** (Motor de Base de Datos)
* **Django ORM** (Modelado y Migraciones)
* **Graphviz & Django Extensions** (Autogeneración del DER del Backend)
* **dbdiagram.io** (Diseño conceptual y lógico rápido)

---

##  Archivos del Módulo BD

| Archivo / Directorio | Descripción |
| :--- | :--- |
| `cafesysdb.sql` | Script SQL base para la creación de las tablas del sistema. |
| `cafesys_backup_total.sql` | Respaldo completo (`pg_dump`) que incluye estructuras y registros. |
| `der_cafesys.png` | Diagrama Entidad-Relación completo autogenerado desde el Backend. |
| `der_cafesys.dot` | Archivo de origen Graphviz para renderizado y edición del DER. |
| `DER-Resumen.png` | Vista compacta/conceptual del DER diseñada en *dbdiagram.io*. |
| `*_rows.csv` | Archivos de datos semilla (`categories`, `products`, `promotions`) para poblar la BD. |
| `README.md` | Documentación técnica del módulo (este archivo). |

---

##  Diagrama Entidad-Relación (DER)

El proyecto cuenta con dos perspectivas de diseño visual:

### 1. DER Detallado (Backend - Graphviz)
Generado automáticamente analizando la metadata de los modelos de Django. Muestra con precisión los tipos de datos exactos de PostgreSQL y las relaciones físicas a nivel de código (`ForeignKey`, `OneToOneField`, etc.).
* **Archivo:** `der_cafesys.png` / `der_cafesys.dot`

### 2. DER Resumen (Conceptual - dbdiagram.io)
Abstracción limpia enfocada en las reglas del negocio e interacciones principales para una lectura rápida en la documentación académica.
* **Archivo:** `DER-Resumen.png`

---

##  Mantenimiento y Comandos Útiles

### Generar o Actualizar el DER dinámicamente
Si realizas cambios en los modelos de Django (`backend/apps/core/models/`), puedes regenerar el archivo `.dot` e imagen ejecutando desde la raíz del **backend**:

```powershell
# Exportar la estructura limpia en formato Graphviz
python manage.py graph_models core -o ..\bd\der_cafesys.dot

# Renderizar directamente a imagen PNG (Requiere Graphviz instalado en el PATH)
python manage.py graph_models core -o ..\bd\der_cafesys.png --rankdir=LR