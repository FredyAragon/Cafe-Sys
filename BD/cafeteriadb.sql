-- ============================================
-- BASE DE DATOS : CAFESYS
-- PostgreSQL
-- MODELO FINAL - 15 TABLAS
-- ============================================

-- ============================================
-- ROLES
-- ============================================
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- USERS
-- ============================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,

    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,

    rol_id INTEGER NOT NULL,

    activo BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_users_roles
        FOREIGN KEY (rol_id)
        REFERENCES roles(id)
        ON DELETE RESTRICT
);

-- ============================================
-- CATEGORIES
-- ============================================
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,

    imagen_url VARCHAR(255),

    activo BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- PRODUCTS
-- ============================================
CREATE TABLE products (
    id SERIAL PRIMARY KEY,

    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,

    precio NUMERIC(10,2) NOT NULL
        CHECK(precio > 0),

    imagen_url VARCHAR(255),

    category_id INTEGER NOT NULL,

    activo BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_products_categories
        FOREIGN KEY (category_id)
        REFERENCES categories(id)
        ON DELETE RESTRICT
);

-- ============================================
-- INVENTORIES
-- ============================================
CREATE TABLE inventories (
    id SERIAL PRIMARY KEY,

    product_id INTEGER NOT NULL,

    stock INTEGER NOT NULL
        CHECK(stock >= 0),

    stock_minimo INTEGER NOT NULL
        CHECK(stock_minimo >= 0),

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_inventories_products
        FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE CASCADE
);

-- ============================================
-- PROMOTIONS
-- ============================================
CREATE TABLE promotions (
    id SERIAL PRIMARY KEY,

    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,

    descuento NUMERIC(5,2) NOT NULL
        CHECK(descuento > 0 AND descuento <= 100),

    tipo_descuento VARCHAR(20) NOT NULL,

    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,

    activo BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_fechas_promotions
        CHECK(fecha_fin >= fecha_inicio)
);

-- ============================================
-- PRODUCTS_PROMOTIONS
-- ============================================
CREATE TABLE products_promotions (
    id SERIAL PRIMARY KEY,

    product_id INTEGER NOT NULL,
    promotion_id INTEGER NOT NULL,

    CONSTRAINT fk_products_promotions_products
        FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_products_promotions_promotions
        FOREIGN KEY (promotion_id)
        REFERENCES promotions(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_products_promotions
        UNIQUE(product_id, promotion_id)
);

-- ============================================
-- LOCATIONS
-- ============================================
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL,

    alias VARCHAR(100),

    direccion VARCHAR(255) NOT NULL,
    referencia TEXT,

    predeterminada BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_locations_users
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- ============================================
-- ORDERS
-- ============================================
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,

    estado VARCHAR(20) NOT NULL,

    total NUMERIC(10,2) NOT NULL
        CHECK(total >= 0),

    notas TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_orders_users
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_orders_locations
        FOREIGN KEY (location_id)
        REFERENCES locations(id)
        ON DELETE RESTRICT
);

-- ============================================
-- ORDER_DETAILS
-- ============================================
CREATE TABLE order_details (
    id SERIAL PRIMARY KEY,

    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,

    cantidad INTEGER NOT NULL
        CHECK(cantidad > 0),

    precio_unitario NUMERIC(10,2) NOT NULL
        CHECK(precio_unitario > 0),

    subtotal NUMERIC(10,2) NOT NULL
        CHECK(subtotal >= 0),

    CONSTRAINT fk_order_details_orders
        FOREIGN KEY (order_id)
        REFERENCES orders(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_order_details_products
        FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE RESTRICT
);

-- ============================================
-- DRIVERS
-- ============================================
CREATE TABLE drivers (
    id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL,

    licencia VARCHAR(50) NOT NULL UNIQUE,

    telefono VARCHAR(20),

    activo BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_drivers_users
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- ============================================
-- VEHICLES
-- ============================================
CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,

    driver_id INTEGER NOT NULL,

    placa VARCHAR(20) NOT NULL UNIQUE,
    modelo VARCHAR(100) NOT NULL,

    activo BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_vehicles_drivers
        FOREIGN KEY (driver_id)
        REFERENCES drivers(id)
        ON DELETE CASCADE
);

-- ============================================
-- DELIVERIES
-- ============================================
CREATE TABLE deliveries (
    id SERIAL PRIMARY KEY,

    order_id INTEGER NOT NULL,
    driver_id INTEGER NOT NULL,
    vehicle_id INTEGER NOT NULL,

    estado VARCHAR(20) NOT NULL,

    fecha_salida TIMESTAMP,
    fecha_entrega TIMESTAMP,

    CONSTRAINT fk_deliveries_orders
        FOREIGN KEY (order_id)
        REFERENCES orders(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_deliveries_drivers
        FOREIGN KEY (driver_id)
        REFERENCES drivers(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_deliveries_vehicles
        FOREIGN KEY (vehicle_id)
        REFERENCES vehicles(id)
        ON DELETE CASCADE
);

-- ============================================
-- REVIEWS
-- ============================================
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,

    calificacion INTEGER NOT NULL
        CHECK(calificacion >= 1 AND calificacion <= 5),

    comentario TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_reviews_users
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_reviews_products
        FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE CASCADE
);

-- ============================================
-- MESSAGES
-- ============================================
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL,

    asunto VARCHAR(150) NOT NULL,
    mensaje TEXT NOT NULL,

    leido BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_messages_users
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- ============================================
-- DATOS DE PRUEBA
-- ============================================

INSERT INTO roles(nombre, descripcion)
VALUES
('Administrador', 'Acceso completo'),
('Cliente', 'Usuario cliente'),
('Repartidor', 'Encargado de entregas');

INSERT INTO categories(nombre)
VALUES
('Cafés'),
('Postres'),
('Bebidas');

INSERT INTO promotions(
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
    'Descuento de verano',
    15,
    'porcentaje',
    '2026-01-01',
    '2026-03-31'
);

INSERT INTO users(
    nombre,
    apellido,
    email,
    password_hash,
    rol_id
)
VALUES
(
    'Fredy',
    'Aragon',
    'fredy@gmail.com',
    '123456',
    1
);