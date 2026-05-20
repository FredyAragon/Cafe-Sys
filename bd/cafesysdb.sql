-- ============================================
-- BASE DE DATOS : CAFESYS
-- PostgreSQL
-- MODELO - 15 TABLAS
-- ============================================

-- ============================================
-- ROLES
-- ============================================
CREATE TABLE roles (
    id          SERIAL       PRIMARY KEY,
    name        VARCHAR(50)  NOT NULL UNIQUE
                    CHECK (TRIM(name) <> ''),
    description TEXT,
    status      VARCHAR(20)  NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'inactive')),
    created     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_id  INTEGER,
    modified_id INTEGER
);

-- ============================================
-- USERS
-- ============================================
CREATE TABLE users (
    id           SERIAL       PRIMARY KEY,
    firstName    VARCHAR(100) NOT NULL
                     CHECK (TRIM(firstName) <> ''),
    lastName     VARCHAR(100) NOT NULL
                     CHECK (TRIM(lastName) <> ''),
    email        VARCHAR(255) NOT NULL UNIQUE
                     CHECK (email LIKE '%@%.%'),
    passwordHash VARCHAR(255) NOT NULL
                     CHECK (LENGTH(passwordHash) >= 8),
    role_id      INTEGER      NOT NULL,
    status       VARCHAR(20)  NOT NULL DEFAULT 'active'
                     CHECK (status IN ('active', 'inactive')),
    created      TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_id   INTEGER,
    modified_id  INTEGER,

    CONSTRAINT fk_users_roles
        FOREIGN KEY (role_id)
        REFERENCES roles(id)
        ON DELETE RESTRICT
);

-- FK de auditoría una vez que users existe
ALTER TABLE roles
    ADD CONSTRAINT fk_roles_created_id  FOREIGN KEY (created_id)  REFERENCES users(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_roles_modified_id FOREIGN KEY (modified_id) REFERENCES users(id) ON DELETE SET NULL;

ALTER TABLE users
    ADD CONSTRAINT fk_users_created_id  FOREIGN KEY (created_id)  REFERENCES users(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_users_modified_id FOREIGN KEY (modified_id) REFERENCES users(id) ON DELETE SET NULL;

-- ============================================
-- CATEGORIES
-- ============================================
CREATE TABLE categories (
    id          SERIAL       PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE
                    CHECK (TRIM(name) <> ''),
    description TEXT,
    imageUrl    VARCHAR(255)
                    CHECK (imageUrl IS NULL OR imageUrl LIKE 'http%'),
    status      VARCHAR(20)  NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'inactive')),
    created     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_id  INTEGER      REFERENCES users(id) ON DELETE SET NULL,
    modified_id INTEGER      REFERENCES users(id) ON DELETE SET NULL
);

-- ============================================
-- PRODUCTS
-- ============================================
CREATE TABLE products (
    id          SERIAL        PRIMARY KEY,
    name        VARCHAR(150)  NOT NULL
                    CHECK (TRIM(name) <> ''),
    description TEXT,
    price       NUMERIC(10,2) NOT NULL
                    CHECK (price > 0),
    imageUrl    VARCHAR(255)
                    CHECK (imageUrl IS NULL OR imageUrl LIKE 'http%'),
    category_id INTEGER       NOT NULL,
    status      VARCHAR(20)   NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'inactive')),
    created     TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_id  INTEGER       REFERENCES users(id) ON DELETE SET NULL,
    modified_id INTEGER       REFERENCES users(id) ON DELETE SET NULL,

    CONSTRAINT fk_products_categories
        FOREIGN KEY (category_id)
        REFERENCES categories(id)
        ON DELETE RESTRICT
);

-- ============================================
-- INVENTORIES
-- ============================================
CREATE TABLE inventories (
    id          SERIAL      PRIMARY KEY,
    product_id  INTEGER     NOT NULL UNIQUE,
    stock       INTEGER     NOT NULL DEFAULT 0
                    CHECK (stock >= 0),
    minStock    INTEGER     NOT NULL DEFAULT 5
                    CHECK (minStock >= 0),
    status      VARCHAR(20) NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'inactive')),
    created     TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_id  INTEGER     REFERENCES users(id) ON DELETE SET NULL,
    modified_id INTEGER     REFERENCES users(id) ON DELETE SET NULL,

    CONSTRAINT fk_inventories_products
        FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE CASCADE
);

-- ============================================
-- PROMOTIONS
-- ============================================
CREATE TABLE promotions (
    id           SERIAL        PRIMARY KEY,
    name         VARCHAR(150)  NOT NULL
                     CHECK (TRIM(name) <> ''),
    description  TEXT,
    discount     NUMERIC(5,2)  NOT NULL
                     CHECK (discount > 0 AND discount <= 100),
    discountType VARCHAR(20)   NOT NULL
                     CHECK (discountType IN ('percentage', 'fixed')),
    startDate    DATE          NOT NULL,
    endDate      DATE          NOT NULL,
    status       VARCHAR(20)   NOT NULL DEFAULT 'active'
                     CHECK (status IN ('active', 'inactive')),
    created      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified     TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_id   INTEGER       REFERENCES users(id) ON DELETE SET NULL,
    modified_id  INTEGER       REFERENCES users(id) ON DELETE SET NULL,

    CONSTRAINT chk_promotions_dates
        CHECK (endDate >= startDate)
);

-- ============================================
-- PRODUCTS_PROMOTIONS
-- ============================================
CREATE TABLE products_promotions (
    product_id   INTEGER   NOT NULL,
    promotion_id INTEGER   NOT NULL,
    status       VARCHAR(20) NOT NULL DEFAULT 'active'
                     CHECK (status IN ('active', 'inactive')),
    created      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_id   INTEGER   REFERENCES users(id) ON DELETE SET NULL,
    modified_id  INTEGER   REFERENCES users(id) ON DELETE SET NULL,

    PRIMARY KEY (product_id, promotion_id),

    CONSTRAINT fk_products_promotions_products
        FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_products_promotions_promotions
        FOREIGN KEY (promotion_id)
        REFERENCES promotions(id)
        ON DELETE CASCADE
);

-- ============================================
-- LOCATIONS
-- ============================================
CREATE TABLE locations (
    id          SERIAL       PRIMARY KEY,
    user_id     INTEGER      NOT NULL,
    alias       VARCHAR(100)
                    CHECK (alias IS NULL OR TRIM(alias) <> ''),
    address     VARCHAR(255) NOT NULL
                    CHECK (TRIM(address) <> ''),
    reference   TEXT,
    isDefault   BOOLEAN      NOT NULL DEFAULT FALSE,
    status      VARCHAR(20)  NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'inactive')),
    created     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_id  INTEGER      REFERENCES users(id) ON DELETE SET NULL,
    modified_id INTEGER      REFERENCES users(id) ON DELETE SET NULL,

    CONSTRAINT fk_locations_users
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- ============================================
-- ORDERS
-- ============================================
CREATE TABLE orders (
    id          SERIAL        PRIMARY KEY,
    user_id     INTEGER       NOT NULL,
    location_id INTEGER       NOT NULL,
    orderStatus VARCHAR(20)   NOT NULL DEFAULT 'pending'
                    CHECK (orderStatus IN (
                        'pending', 'preparing', 'ready', 'delivered', 'cancelled'
                    )),
    total       NUMERIC(10,2) NOT NULL
                    CHECK (total >= 0),
    notes       TEXT,
    status      VARCHAR(20)   NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'inactive')),
    created     TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_id  INTEGER       REFERENCES users(id) ON DELETE SET NULL,
    modified_id INTEGER       REFERENCES users(id) ON DELETE SET NULL,

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
    id          SERIAL        PRIMARY KEY,
    order_id    INTEGER       NOT NULL,
    product_id  INTEGER       NOT NULL,
    quantity    INTEGER       NOT NULL
                    CHECK (quantity > 0),
    unitPrice   NUMERIC(10,2) NOT NULL
                    CHECK (unitPrice > 0),
    subtotal    NUMERIC(10,2) NOT NULL
                    CHECK (subtotal >= 0),
    status      VARCHAR(20)   NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'inactive')),
    created     TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_id  INTEGER       REFERENCES users(id) ON DELETE SET NULL,
    modified_id INTEGER       REFERENCES users(id) ON DELETE SET NULL,

    UNIQUE (order_id, product_id),

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
    id          SERIAL      PRIMARY KEY,
    user_id     INTEGER     NOT NULL UNIQUE,
    license     VARCHAR(50) NOT NULL UNIQUE
                    CHECK (TRIM(license) <> ''),
    phone       VARCHAR(20)
                    CHECK (phone IS NULL OR LENGTH(phone) >= 7),
    status      VARCHAR(20) NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'inactive')),
    created     TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_id  INTEGER     REFERENCES users(id) ON DELETE SET NULL,
    modified_id INTEGER     REFERENCES users(id) ON DELETE SET NULL,

    CONSTRAINT fk_drivers_users
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- ============================================
-- VEHICLES
-- ============================================
CREATE TABLE vehicles (
    id          SERIAL       PRIMARY KEY,
    driver_id   INTEGER      NOT NULL,
    plate       VARCHAR(20)  NOT NULL UNIQUE
                    CHECK (TRIM(plate) <> ''),
    model       VARCHAR(100) NOT NULL
                    CHECK (TRIM(model) <> ''),
    status      VARCHAR(20)  NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'inactive')),
    created     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_id  INTEGER      REFERENCES users(id) ON DELETE SET NULL,
    modified_id INTEGER      REFERENCES users(id) ON DELETE SET NULL,

    CONSTRAINT fk_vehicles_drivers
        FOREIGN KEY (driver_id)
        REFERENCES drivers(id)
        ON DELETE CASCADE
);

-- ============================================
-- DELIVERIES
-- ============================================
CREATE TABLE deliveries (
    id             SERIAL      PRIMARY KEY,
    order_id       INTEGER     NOT NULL UNIQUE,
    driver_id      INTEGER     NOT NULL,
    vehicle_id     INTEGER     NOT NULL,
    deliveryStatus VARCHAR(20) NOT NULL DEFAULT 'pending'
                       CHECK (deliveryStatus IN (
                           'pending', 'on_the_way', 'delivered', 'failed'
                       )),
    departureAt    TIMESTAMP,
    deliveredAt    TIMESTAMP,
    status         VARCHAR(20) NOT NULL DEFAULT 'active'
                       CHECK (status IN ('active', 'inactive')),
    created        TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified       TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_id     INTEGER     REFERENCES users(id) ON DELETE SET NULL,
    modified_id    INTEGER     REFERENCES users(id) ON DELETE SET NULL,

    CONSTRAINT chk_deliveries_dates
        CHECK (deliveredAt IS NULL OR deliveredAt >= departureAt),

    CONSTRAINT fk_deliveries_orders
        FOREIGN KEY (order_id)
        REFERENCES orders(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_deliveries_drivers
        FOREIGN KEY (driver_id)
        REFERENCES drivers(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_deliveries_vehicles
        FOREIGN KEY (vehicle_id)
        REFERENCES vehicles(id)
        ON DELETE RESTRICT
);

-- ============================================
-- REVIEWS
-- ============================================
CREATE TABLE reviews (
    id          SERIAL      PRIMARY KEY,
    user_id     INTEGER     NOT NULL,
    product_id  INTEGER     NOT NULL,
    rating      SMALLINT    NOT NULL
                    CHECK (rating BETWEEN 1 AND 5),
    comment     TEXT,
    status      VARCHAR(20) NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'inactive')),
    created     TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_id  INTEGER     REFERENCES users(id) ON DELETE SET NULL,
    modified_id INTEGER     REFERENCES users(id) ON DELETE SET NULL,

    UNIQUE (user_id, product_id),

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
    id          SERIAL       PRIMARY KEY,
    user_id     INTEGER,
    subject     VARCHAR(150) NOT NULL
                    CHECK (TRIM(subject) <> ''),
    body        TEXT         NOT NULL
                    CHECK (TRIM(body) <> ''),
    isRead      BOOLEAN      NOT NULL DEFAULT FALSE,
    status      VARCHAR(20)  NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'inactive')),
    created     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_id  INTEGER      REFERENCES users(id) ON DELETE SET NULL,
    modified_id INTEGER      REFERENCES users(id) ON DELETE SET NULL,

    CONSTRAINT fk_messages_users
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL
);

-- ============================================
-- ÍNDICES
-- ============================================
CREATE INDEX idx_users_email          ON users(email);
CREATE INDEX idx_users_role           ON users(role_id);
CREATE INDEX idx_products_category    ON products(category_id);
CREATE INDEX idx_inventories_product  ON inventories(product_id);
CREATE INDEX idx_orders_user          ON orders(user_id);
CREATE INDEX idx_orders_location      ON orders(location_id);
CREATE INDEX idx_order_details_order  ON order_details(order_id);
CREATE INDEX idx_locations_user       ON locations(user_id);
CREATE INDEX idx_drivers_user         ON drivers(user_id);
CREATE INDEX idx_vehicles_driver      ON vehicles(driver_id);
CREATE INDEX idx_deliveries_order     ON deliveries(order_id);
CREATE INDEX idx_reviews_product      ON reviews(product_id);

-- ============================================
-- DATOS DE PRUEBA
-- ============================================
INSERT INTO roles (name, description) VALUES
    ('Administrator', 'Full system access'),
    ('Client',        'Customer who places orders'),
    ('Driver',        'Delivery person');

INSERT INTO categories (name) VALUES
    ('Hot Coffees'),
    ('Cold Drinks'),
    ('Desserts'),
    ('Sandwiches');

INSERT INTO promotions (name, description, discount, discountType, startDate, endDate) VALUES
    ('Summer Sale', 'Summer discount', 15.00, 'percentage', '2026-01-01', '2026-03-31'),
    ('2x1 Coffees', 'Buy one get one', 50.00, 'percentage', '2026-05-01', '2026-05-31');

INSERT INTO users (firstName, lastName, email, passwordHash, role_id) VALUES
    ('Fredy', 'Aragon', 'fredy@gmail.com', 'hashed_password_here', 1);