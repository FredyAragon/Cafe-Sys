-- =============================================
-- bd.sql — Cafetería
-- Tablas basadas en models.py
-- =============================================

-- ── 1. roles ─────────────────────────────────
CREATE TABLE roles (
    id          SERIAL PRIMARY KEY,
    nombre      VARCHAR(50)  NOT NULL UNIQUE,
    descripcion TEXT,
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ── 2. usuarios ──────────────────────────────
CREATE TABLE usuarios (
    id            SERIAL PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL,
    apellido      VARCHAR(100) NOT NULL,
    email         VARCHAR(254) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol_id        INTEGER      NOT NULL REFERENCES roles(id) ON DELETE PROTECT,
    activo        BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ── 3. categorias ────────────────────────────
CREATE TABLE categorias (
    id          SERIAL PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    descripcion TEXT,
    imagen_url  VARCHAR(255),
    activo      BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ── 4. productos ─────────────────────────────
CREATE TABLE productos (
    id          SERIAL PRIMARY KEY,
    nombre      VARCHAR(150)  NOT NULL,
    descripcion TEXT,
    precio      NUMERIC(10,2) NOT NULL CHECK (precio > 0),
    imagen_url  VARCHAR(255),
    categoria_id INTEGER      NOT NULL REFERENCES categorias(id) ON DELETE RESTRICT,
    activo      BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP     NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP     NOT NULL DEFAULT NOW()
);

-- ── 5. ingredientes ──────────────────────────
CREATE TABLE ingredientes (
    id            SERIAL PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL,
    unidad_medida VARCHAR(20)  NOT NULL,
    activo        BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ── 6. promociones ───────────────────────────
CREATE TABLE promociones (
    id             SERIAL PRIMARY KEY,
    nombre         VARCHAR(150)  NOT NULL,
    descripcion    TEXT,
    descuento      NUMERIC(5,2)  NOT NULL CHECK (descuento > 0 AND descuento <= 100),
    tipo_descuento VARCHAR(20)   NOT NULL,
    fecha_inicio   DATE          NOT NULL,
    fecha_fin      DATE          NOT NULL CHECK (fecha_fin > fecha_inicio),
    activo         BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at     TIMESTAMP     NOT NULL DEFAULT NOW()
);

-- ── 7. departamentos ─────────────────────────
CREATE TABLE departamentos (
    id     SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- ── 8. provincias ────────────────────────────
CREATE TABLE provincias (
    id               SERIAL PRIMARY KEY,
    nombre           VARCHAR(100) NOT NULL,
    departamento_id  INTEGER      NOT NULL REFERENCES departamentos(id) ON DELETE CASCADE
);

-- ── 9. vehiculos ─────────────────────────────
CREATE TABLE vehiculos (
    id     SERIAL PRIMARY KEY,
    placa  VARCHAR(20)  NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    activo BOOLEAN      NOT NULL DEFAULT TRUE
);

-- ── 10. ubicaciones ──────────────────────────
CREATE TABLE ubicaciones (
    id             SERIAL PRIMARY KEY,
    usuario_id     INTEGER      NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    alias          VARCHAR(100),
    direccion      VARCHAR(255) NOT NULL,
    referencia     TEXT,
    predeterminada BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at     TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ── 11. pedidos ──────────────────────────────
CREATE TABLE pedidos (
    id           SERIAL PRIMARY KEY,
    usuario_id   INTEGER       NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    ubicacion_id INTEGER       NOT NULL REFERENCES ubicaciones(id) ON DELETE RESTRICT,
    estado       VARCHAR(20)   NOT NULL DEFAULT 'pendiente'
                     CHECK (estado IN (
                         'pendiente','en_preparacion',
                         'listo','entregado','cancelado'
                     )),
    total        NUMERIC(10,2) NOT NULL CHECK (total >= 0),
    notas        TEXT,
    created_at   TIMESTAMP     NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMP     NOT NULL DEFAULT NOW()
);

-- ── 12. detalle_pedidos ──────────────────────
CREATE TABLE detalle_pedidos (
    id             SERIAL PRIMARY KEY,
    pedido_id      INTEGER       NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
    producto_id    INTEGER       NOT NULL REFERENCES productos(id) ON DELETE RESTRICT,
    cantidad       INTEGER       NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(10,2) NOT NULL,
    subtotal       NUMERIC(10,2) NOT NULL,
    UNIQUE (pedido_id, producto_id)
);

-- ── 13. producto_ingrediente (N:M) ───────────
CREATE TABLE producto_ingrediente (
    producto_id    INTEGER       NOT NULL REFERENCES productos(id) ON DELETE CASCADE,
    ingrediente_id INTEGER       NOT NULL REFERENCES ingredientes(id) ON DELETE CASCADE,
    cantidad       NUMERIC(10,2) NOT NULL CHECK (cantidad > 0),
    PRIMARY KEY (producto_id, ingrediente_id)
);

-- ── 14. producto_promocion (N:M) ─────────────
CREATE TABLE producto_promocion (
    producto_id  INTEGER NOT NULL REFERENCES productos(id) ON DELETE CASCADE,
    promocion_id INTEGER NOT NULL REFERENCES promociones(id) ON DELETE CASCADE,
    PRIMARY KEY (producto_id, promocion_id)
);

-- =============================================
-- Datos de prueba
-- =============================================

INSERT INTO roles (nombre, descripcion) VALUES
    ('admin',   'Administrador con acceso total'),
    ('cliente', 'Usuario que realiza pedidos');

INSERT INTO categorias (nombre) VALUES
    ('Cafés Calientes'),
    ('Bebidas Frías'),
    ('Postres'),
    ('Bocadillos');

INSERT INTO departamentos (nombre) VALUES
    ('Arequipa'),
    ('Lima');

INSERT INTO provincias (nombre, departamento_id) VALUES
    ('Arequipa', 1),
    ('Lima',     2);

INSERT INTO ingredientes (nombre, unidad_medida) VALUES
    ('Café molido', 'g'),
    ('Leche',       'ml'),
    ('Azúcar',      'g'),
    ('Crema de queso', 'g'),
    ('Pan de molde', 'unidad');

INSERT INTO promociones (nombre, descuento, tipo_descuento, fecha_inicio, fecha_fin) VALUES
    ('Descuento Verano', 10.00, 'porcentaje', '2026-01-01', '2026-03-31'),
    ('2x1 Cafés',        50.00, 'porcentaje', '2026-05-01', '2026-05-31');