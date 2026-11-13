CREATE DATABASE IF NOT EXISTS moscato_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE moscato_db;

-- =========================
-- TABLA CATEGORIAS (NUEVA)
-- =========================
-- Almacena las clasificaciones del menú de forma dinámica
CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT NULL,
    activo TINYINT(1) DEFAULT 1,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =========================
-- TABLA EMPLEADOS (NUEVA)
-- =========================
-- Almacena los datos fisicos y de contacto del personal
CREATE TABLE IF NOT EXISTS empleados (
    id_empleado INT PRIMARY KEY AUTO_INCREMENT,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL, 
    documento_identidad VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20) NULL,
    cargo VARCHAR(50) NOT NULL,
    activo TINYINT(1) DEFAULT 1,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =========================
-- TABLA USUARIOS (MODIFICADA)
-- =========================
-- Se eliminó "nombre" y se agregó "id_empleado" para normalizar
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    id_empleado INT NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol ENUM('Administrador', 'Mesero', 'Cocinero') NOT NULL,
    activo TINYINT(1) DEFAULT 1,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
);

-- =========================
-- TABLA AUDITORIA
-- =========================
CREATE TABLE IF NOT EXISTS auditoria (
    id_registro INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    accion VARCHAR(50) NOT NULL,
    tabla_afectada VARCHAR(100) NOT NULL,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    detalles TEXT NULL,

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- =========================
-- TABLA MESAS
-- =========================
CREATE TABLE IF NOT EXISTS mesas (
    id_mesa INT PRIMARY KEY AUTO_INCREMENT,
    numero_mesa INT UNIQUE NOT NULL,
    estado ENUM('Libre', 'Atencion', 'Ocupada', 'Inactiva') DEFAULT 'Libre',
    activo TINYINT(1) DEFAULT 1,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =========================
-- TABLA PRODUCTOS (MODIFICADA)
-- =========================
-- Se cambió el ENUM 'categoria' por la llave foránea 'id_categoria'
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255) NULL,
    precio DECIMAL(10, 2) NOT NULL,
    id_categoria INT NOT NULL,
    disponible TINYINT(1) DEFAULT 1,
    activo TINYINT(1) DEFAULT 1,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);


-- =========================
-- TABLA PEDIDOS
-- =========================
CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido INT PRIMARY KEY AUTO_INCREMENT,
    id_mesa INT NULL,
    id_usuario INT NOT NULL,
    tipo_pedido ENUM('Mesa', 'Para llevar') DEFAULT 'Mesa',
    fecha_apertura DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_cierre DATETIME NULL,
    subtotal_consumido DECIMAL(10, 2) DEFAULT 0.00,
    estado_pedido ENUM('Abierto', 'En cocina', 'Listo', 'Servido', 'Cancelado') DEFAULT 'Abierto',
    pagado TINYINT(1) DEFAULT 0,
    metodo_pago VARCHAR(30) NULL,

    FOREIGN KEY (id_mesa) REFERENCES mesas(id_mesa),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- Compatibilidad con bases creadas antes de agregar los datos de pago.
ALTER TABLE pedidos
    ADD COLUMN IF NOT EXISTS pagado TINYINT(1) DEFAULT 0,
    ADD COLUMN IF NOT EXISTS metodo_pago VARCHAR(30) NULL;

-- =========================
-- TABLA RELACION PEDIDOS/TICKETS
-- =========================
CREATE TABLE IF NOT EXISTS pedidos_ticket_map (
    id_pedido INT PRIMARY KEY,
    ticket_numero INT NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido)
);

-- =========================
-- TABLA DETALLE_PEDIDO
-- =========================
CREATE TABLE IF NOT EXISTS detalle_pedido (
    id_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    descripcion_preparacion TEXT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    fecha_envio_cocina DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado_item ENUM('Pendiente', 'En cocina', 'En preparación', 'Listo', 'Servido', 'Cancelado') DEFAULT 'Pendiente',    oculto_cocina TINYINT(1) DEFAULT 0,

    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- =========================
-- DATOS INICIALES
-- =========================
INSERT INTO categorias (id_categoria, nombre, descripcion) VALUES
(1, 'Moscato Chino - Compartir', 'Combos y para compartir de comida china'),
(2, 'Moscato Chino - Personal', 'Platos individuales de comida china y acompañantes'),
(3, 'Moscato Broaster', 'Combos de pollo a la broaster tradicional'),
(4, 'Promociones', 'Ofertas especiales y combos mixtos'),
(5, 'Bebidas', 'Refrescos, jugos y merengadas');

INSERT INTO empleados (id_empleado, nombres, apellidos, documento_identidad, telefono, cargo, activo) VALUES
(1, 'manuel', 'castro', '00000000', '00000000', 'Administrador', 1),
(2, 'manuel', 'castro', '30000000', '00000000', 'Cocinero', 1),
(3, 'manuel', 'castro', '123456789', '123456789', 'Mesero', 1),
(19, 'manuel', 'castro', 'USR-admin', NULL, 'Administrador', 1),
(20, 'mesero', 'Sin apellido', 'USR-mesero1', NULL, 'Mesero', 1),
(21, 'mesero', 'Sin apellido', 'USR-mesero2', NULL, 'Mesero', 1),
(22, 'cocinero', 'Sin apellido', 'USR-cocinero1', NULL, 'Cocinero', 1),
(23, 'cocinero', 'Sin apellido', 'USR-cocinero2', NULL, 'Cocinero', 1);

INSERT INTO usuarios (id_usuario, id_empleado, username, password, rol, activo) VALUES
(7, 19, 'admin', '123', 'Administrador', 1),
(8, 20, 'mesero1', '0000', 'Mesero', 1),
(9, 21, 'mesero2', '0000', 'Mesero', 1),
(10, 22, 'cocinero1', '0000', 'Cocinero', 1),
(11, 23, 'cocinero2', '0000', 'Cocinero', 1);

INSERT INTO mesas (id_mesa, numero_mesa, estado, activo) VALUES
(1, 1, 'Libre', 1),
(2, 2, 'Libre', 1),
(3, 3, 'Libre', 1),
(4, 4, 'Libre', 1),
(5, 5, 'Libre', 1),
(6, 6, 'Libre', 1),
(7, 7, 'Libre', 1),
(8, 8, 'Libre', 1),
(9, 9, 'Libre', 1),
(10, 10, 'Libre', 1);

INSERT INTO productos (id_producto, nombre, descripcion, precio, id_categoria) VALUES
(1, 'Combo 1', 'Arroz 500 g, 3 piezas de pollo broaster y 3 lumpias', 36000.00, 1),
(2, 'Combo 2', 'Arroz 1 kg y 4 lumpias', 39000.00, 1),
(3, 'Combo 3', '8 piezas de pollo broaster, arroz 1 kg y 4 lumpias', 70000.00, 1),
(4, 'Combo 4', 'Pollo agridulce, chop suey, arroz 1 kg y 4 lumpias', 60000.00, 1),
(5, 'Combo 5', 'Arroz 1.5 kg, 8 piezas de pollo, chop suey, 5 lumpias y refresco', 130000.00, 1),
(6, 'Promo Personal', 'Arroz 150 g y 1 lumpia', 8000.00, 2),
(7, 'Chop Suey', 'Chop suey, arroz 250 g, 1 lumpia y papas fritas', 15000.00, 2),
(8, 'Pollo Agridulce', 'Pollo agridulce, arroz 250 g, 1 lumpia y papas', 20000.00, 2),
(9, 'Pollo Broaster Personal', '2 piezas de pollo broaster, arroz 250 g, 1 lumpia y papas', 20000.00, 2),
(10, 'Cerdo Agridulce', 'Cerdo agridulce, arroz 250 g, 1 lumpia y papas', 26000.00, 2),
(11, 'Lomito en Salsa de Ostras', 'Lomito en salsa de ostras, arroz 250 g, 1 lumpia y papas', 26000.00, 2),
(12, 'Combo Soltero', '1 pieza de pollo crocante y arepitas', 10000.00, 3),
(13, 'Combo Dúo', '2 piezas de pollo crocante y arepitas', 14000.00, 3),
(14, 'Combo Mediano', '4 piezas de pollo crocante y arepitas', 28000.00, 3),
(15, 'Combo Broaster', '8 piezas de pollo, arepitas y papas', 59000.00, 3),
(16, 'Combo Especial', '8 piezas de pollo, 10 arepitas, papas, ensalada y refresco de 1 litro', 55000.00, 4),
(17, 'Súper Moscato', 'Arroz especial, pollo broaster y lumpias', 70000.00, 4),
(30, 'refresco 300ml', 'botella', 3000.00, 5),
(31, 'refresco 1 litro', 'botella', 6000.00, 5),
(32, 'refresco 1.25 litros', 'botella', 6000.00, 5),
(33, 'refresco 2 litros', 'botella', 8000.00, 5),
(34, 'merengada fresa', '', 8000.00, 5),
(35, 'merengada guanabana', '', 8000.00, 5),
(36, 'merengada mora', '', 8000.00, 5),
(37, 'merengad mango', '', 8000.00, 5),
(38, 'jugo fresa', '', 8000.00, 5),
(39, 'jugo guanabana', '', 8000.00, 5),
(40, 'jugo mora', '', 8000.00, 5),
(41, 'jugo mango', '', 8000.00, 5),
(42, 'Serv. lumpias', '', 12000.00, 2);
-- =========================
-- ÍNDICES PARA RENDIMIENTO
-- =========================
ALTER TABLE mesas ADD INDEX idx_mesas_estado (estado);
ALTER TABLE pedidos ADD INDEX idx_pedidos_estado (estado_pedido);
ALTER TABLE pedidos ADD INDEX idx_pedidos_fechas (fecha_apertura, fecha_cierre);
ALTER TABLE detalle_pedido ADD INDEX idx_detalle_estado (estado_item);



