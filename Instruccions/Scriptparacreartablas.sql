-- ROLES
CREATE TABLE roles (
    id INT IDENTITY PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    created_at DATETIME DEFAULT GETDATE()
);

-- USUARIOS
CREATE TABLE usuarios (
    id INT IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol_id INT NOT NULL,
    activo BIT DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME,
    FOREIGN KEY (rol_id) REFERENCES roles(id)
);
CREATE TABLE categorias (
    id INT IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    imagen_url VARCHAR(255),
    activo BIT DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE productos (
    id INT IDENTITY PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    imagen_url VARCHAR(255),
    categoria_id INT NOT NULL,
    activo BIT DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE inventario (
    id INT IDENTITY PRIMARY KEY,
    producto_id INT UNIQUE NOT NULL,
    stock INT NOT NULL,
    stock_minimo INT NOT NULL,
    updated_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);
CREATE TABLE promociones (
    id INT IDENTITY PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    descuento DECIMAL(5,2) NOT NULL,
    tipo_descuento VARCHAR(20) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    activo BIT DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE producto_promocion (
    producto_id INT NOT NULL,
    promocion_id INT NOT NULL,
    PRIMARY KEY (producto_id, promocion_id),
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    FOREIGN KEY (promocion_id) REFERENCES promociones(id)
);

CREATE TABLE ingredientes (
    id INT IDENTITY PRIMARY KEY,
    nombre VARCHAR(100),
    unidad_medida VARCHAR(20),
    activo BIT DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE inventario_ingredientes (
    id INT IDENTITY PRIMARY KEY,
    ingrediente_id INT UNIQUE,
    stock DECIMAL(10,2),
    stock_minimo DECIMAL(10,2),
    updated_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id)
);

CREATE TABLE ubicaciones (
    id INT IDENTITY PRIMARY KEY,
    usuario_id INT NOT NULL,
    alias VARCHAR(100),
    direccion VARCHAR(255) NOT NULL,
    distrito_id INT,
    referencia TEXT,
    predeterminada BIT DEFAULT 0,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE pedidos (
    id INT IDENTITY PRIMARY KEY,
    usuario_id INT NOT NULL,
    ubicacion_id INT NOT NULL,
    estado VARCHAR(20) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    notas TEXT,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (ubicacion_id) REFERENCES ubicaciones(id)
);

CREATE TABLE detalle_pedidos (
    id INT IDENTITY PRIMARY KEY,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE carrito (
    id INT IDENTITY PRIMARY KEY,
    usuario_id INT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE carrito_detalle (
    carrito_id INT,
    producto_id INT,
    cantidad INT NOT NULL,
    PRIMARY KEY (carrito_id, producto_id),
    FOREIGN KEY (carrito_id) REFERENCES carrito(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE repartidores (
    id INT IDENTITY PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    telefono VARCHAR(20),
    activo BIT DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE envios (
    id INT IDENTITY PRIMARY KEY,
    pedido_id INT UNIQUE NOT NULL,
    repartidor_id INT,
    estado VARCHAR(20),
    costo_envio DECIMAL(10,2),
    fecha_entrega DATETIME,
    notas TEXT,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (repartidor_id) REFERENCES repartidores(id)
);

CREATE TABLE resenas (
    id INT IDENTITY PRIMARY KEY,
    usuario_id INT NOT NULL,
    producto_id INT NOT NULL,
    calificacion SMALLINT,
    comentario TEXT,
    activo BIT DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE mensajes (
    id INT IDENTITY PRIMARY KEY,
    usuario_id INT NOT NULL,
    asunto VARCHAR(150),
    mensaje TEXT,
    leido BIT DEFAULT 0,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE producto_ingrediente (
    producto_id INT,
    ingrediente_id INT,
    cantidad DECIMAL(10,2),
    PRIMARY KEY (producto_id, ingrediente_id),
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id)
);

CREATE TABLE producciones (
    id INT IDENTITY PRIMARY KEY,
    producto_id INT,
    usuario_id INT,
    cantidad_producida INT,
    notas TEXT,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
