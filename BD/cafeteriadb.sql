-- ============================================
-- BASE DE DATOS : CAFESYS
-- PostgreSQL
-- ============================================

-- =========================
-- ROLES
-- =========================
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- USUARIOS
-- =========================
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,

    rol_id INTEGER NOT NULL,
    
    activo BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_usuarios_roles
        FOREIGN KEY (rol_id)
        REFERENCES roles(id)
        ON DELETE RESTRICT
);

-- =========================
-- CATEGORIAS
-- =========================
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    imagen_url VARCHAR(255),

    activo BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- PRODUCTOS
-- =========================
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,

    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,

    precio NUMERIC(10,2) NOT NULL
        CHECK (precio > 0),

    imagen_url VARCHAR(255),

    categoria_id INTEGER NOT NULL,

    activo BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_productos_categorias
        FOREIGN KEY (categoria_id)
        REFERENCES categorias(id)
        ON DELETE RESTRICT
);

-- =========================
-- INGREDIENTES
-- =========================
CREATE TABLE ingredientes (
    id SERIAL PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,
    unidad_medida VARCHAR(20) NOT NULL,

    activo BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- PROMOCIONES
-- =========================
CREATE TABLE promociones (
    id SERIAL PRIMARY KEY,

    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,

    descuento NUMERIC(5,2) NOT NULL
        CHECK (descuento > 0 AND descuento <= 100),

    tipo_descuento VARCHAR(20) NOT NULL,

    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,

    activo BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_fechas_promocion
        CHECK (fecha_fin >= fecha_inicio)
);

-- =========================
-- DEPARTAMENTOS
-- =========================
CREATE TABLE departamentos (
    id SERIAL PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL
);

-- =========================
-- PROVINCIAS
-- =========================
CREATE TABLE provincias (
    id SERIAL PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    departamento_id INTEGER NOT NULL,

    CONSTRAINT fk_provincias_departamentos
        FOREIGN KEY (departamento_id)
        REFERENCES departamentos(id)
        ON DELETE CASCADE
);

-- =========================
-- VEHICULOS
-- =========================
CREATE TABLE vehiculos (
    id SERIAL PRIMARY KEY,

    placa VARCHAR(20) NOT NULL UNIQUE,
    modelo VARCHAR(100) NOT NULL,

    activo BOOLEAN NOT NULL DEFAULT TRUE
);

-- =========================
-- UBICACIONES
-- =========================
CREATE TABLE ubicaciones (
    id SERIAL PRIMARY KEY,

    usuario_id INTEGER NOT NULL,

    alias VARCHAR(100),

    direccion VARCHAR(255) NOT NULL,

    referencia TEXT,

    predeterminada BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_ubicaciones_usuarios
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
);

-- =========================
-- PEDIDOS
-- =========================
CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,

    usuario_id INTEGER NOT NULL,
    ubicacion_id INTEGER NOT NULL,

    estado VARCHAR(20) NOT NULL,

    total NUMERIC(10,2) NOT NULL
        CHECK (total >= 0),

    notas TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_pedidos_usuarios
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_pedidos_ubicaciones
        FOREIGN KEY (ubicacion_id)
        REFERENCES ubicaciones(id)
        ON DELETE RESTRICT
);

-- =========================
-- DETALLE_PEDIDOS
-- =========================
CREATE TABLE detalle_pedidos (
    id SERIAL PRIMARY KEY,

    pedido_id INTEGER,
    producto_id INTEGER,

    cantidad INTEGER
        CHECK (cantidad > 0),

    precio_unitario NUMERIC(10,2)
        CHECK (precio_unitario > 0),

    subtotal NUMERIC(10,2)
        CHECK (subtotal >= 0),

    CONSTRAINT fk_detalle_pedidos_pedidos
        FOREIGN KEY (pedido_id)
        REFERENCES pedidos(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_detalle_pedidos_productos
        FOREIGN KEY (producto_id)
        REFERENCES productos(id)
        ON DELETE RESTRICT
);

-- =========================
-- PRODUCTO_INGREDIENTE
-- =========================
CREATE TABLE producto_ingrediente (
    id SERIAL PRIMARY KEY,

    producto_id INTEGER NOT NULL,
    ingrediente_id INTEGER NOT NULL,

    cantidad NUMERIC(10,2) NOT NULL
        CHECK (cantidad > 0),

    CONSTRAINT fk_producto_ingrediente_productos
        FOREIGN KEY (producto_id)
        REFERENCES productos(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_producto_ingrediente_ingredientes
        FOREIGN KEY (ingrediente_id)
        REFERENCES ingredientes(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_producto_ingrediente
        UNIQUE(producto_id, ingrediente_id)
);

-- =========================
-- PRODUCTO_PROMOCION
-- =========================
CREATE TABLE producto_promocion (
    id SERIAL PRIMARY KEY,

    producto_id INTEGER NOT NULL,
    promocion_id INTEGER NOT NULL,

    CONSTRAINT fk_producto_promocion_productos
        FOREIGN KEY (producto_id)
        REFERENCES productos(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_producto_promocion_promociones
        FOREIGN KEY (promocion_id)
        REFERENCES promociones(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_producto_promocion
        UNIQUE(producto_id, promocion_id)
);

-- ============================================
-- DATOS DE PRUEBA
-- ============================================

INSERT INTO roles(nombre, descripcion)
VALUES
('Administrador', 'Acceso completo'),
('Cliente', 'Usuario cliente');

INSERT INTO categorias(nombre)
VALUES
('Cafés'),
('Postres'),
('Bebidas');

INSERT INTO departamentos(nombre)
VALUES
('Arequipa'),
('Lima');

INSERT INTO provincias(nombre, departamento_id)
VALUES
('Arequipa', 1),
('Lima', 2);

INSERT INTO ingredientes(nombre, unidad_medida)
VALUES
('Cafe molido', 'g'),
('Leche', 'ml'),
('Azucar', 'g');

INSERT INTO promociones(
    nombre,
    descripcion,
    descuento,
    tipo_descuento,
    fecha_inicio,
    fecha_fin
)
VALUES
(
    'Promo Verano',
    'Descuento temporada verano',
    15,
    'porcentaje',
    '2026-01-01',
    '2026-03-31'
);