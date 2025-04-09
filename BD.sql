
-- crear BD
CREATE DATABASE parking_management;

-- Create tables
CREATE TABLE distrito (
    id_distrito SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo_postal VARCHAR(10),
    ciudad VARCHAR(100)
);

CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE duenos (
    id_dueno SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cochera (
    id_cochera SERIAL PRIMARY KEY,
    direccion VARCHAR(255) NOT NULL,
    capacidad INTEGER NOT NULL,
    precio_hora DECIMAL(10, 2) NOT NULL,
    disponible BOOLEAN DEFAULT TRUE,
    id_distrito INTEGER REFERENCES distrito(id_distrito),
    id_dueno INTEGER REFERENCES duenos(id_dueno)
);

CREATE TABLE pagos (
    id_pago SERIAL PRIMARY KEY,
    monto DECIMAL(10, 2) NOT NULL,
    fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metodo_pago VARCHAR(50),
    id_usuario INTEGER REFERENCES usuario(id_usuario),
    id_dueno INTEGER REFERENCES duenos(id_dueno)
);

CREATE TABLE calificacion (
    id_calificacion SERIAL PRIMARY KEY,
    puntuacion INTEGER NOT NULL CHECK (puntuacion >= 1 AND puntuacion <= 5),
    comentario TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER REFERENCES usuario(id_usuario),
    id_cochera INTEGER REFERENCES cochera(id_cochera)
);

CREATE TABLE reserva (
    id_reserva SERIAL PRIMARY KEY,
    fecha_inicio TIMESTAMP NOT NULL,
    fecha_fin TIMESTAMP NOT NULL,
    estado VARCHAR(50) DEFAULT 'pendiente',
    id_usuario INTEGER REFERENCES usuario(id_usuario),
    id_cochera INTEGER REFERENCES cochera(id_cochera),
    CHECK (fecha_fin > fecha_inicio)
);

-- Crear tabla para los registro
CREATE TABLE registros_cochera (
    id_registro SERIAL PRIMARY KEY,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    detalles TEXT,
    id_cochera INTEGER REFERENCES cochera(id_cochera),
    id_dueno INTEGER REFERENCES duenos(id_dueno)
);

-- Indexamos las tablas
CREATE INDEX idx_cochera_distrito ON cochera(id_distrito);
CREATE INDEX idx_cochera_dueno ON cochera(id_dueno);
CREATE INDEX idx_reserva_usuario ON reserva(id_usuario);
CREATE INDEX idx_reserva_cochera ON reserva(id_cochera);
CREATE INDEX idx_pago_usuario ON pagos(id_usuario);
CREATE INDEX idx_calificacion_cochera ON calificacion(id_cochera);

-- Testeamos con un poco de data
INSERT INTO distrito (nombre, codigo_postal, ciudad) VALUES 
('Miraflores', '15046', 'Lima'),
('San Isidro', '15073', 'Lima'),
('Barranco', '15063', 'Lima'),
('Surco', '15038', 'Lima'),
('San Borja', '15036', 'Lima'),
('La Molina', '15026', 'Lima');

INSERT INTO usuario (nombre, apellido, email, telefono) VALUES
('Juan', 'Pérez', 'juan.perez@email.com', '+51987654321'),
('María', 'García', 'maria.garcia@email.com', '+51987654322'),
('Roberto', 'Sánchez', 'roberto.sanchez@email.com', '+51987654325'),
('Carmen', 'Mendoza', 'carmen.mendoza@email.com', '+51987654326'),
('Luis', 'Torres', 'luis.torres@email.com', '+51987654327'),
('Patricia', 'Ríos', 'patricia.rios@email.com', '+51987654328'),
('Jorge', 'Vargas', 'jorge.vargas@email.com', '+51987654329');

INSERT INTO duenos (nombre, apellido, email, telefono) VALUES
('Carlos', 'Rodríguez', 'carlos.rodriguez@email.com', '+51987654323'),
('Ana', 'López', 'ana.lopez@email.com', '+51987654324'),
('Miguel', 'Castro', 'miguel.castro@email.com', '+51987654330'),
('Laura', 'Guzmán', 'laura.guzman@email.com', '+51987654331'),
('Fernando', 'Paredes', 'fernando.paredes@email.com', '+51987654332'),
('Susana', 'Ortiz', 'susana.ortiz@email.com', '+51987654333');


-- Datos para la tabla cochera
INSERT INTO cochera (direccion, capacidad, precio_hora, disponible, id_distrito, id_dueno) VALUES
('Av. Larco 345', 10, 12.50, true, 1, 1),
('Calle Las Flores 123', 5, 10.00, true, 2, 2),
('Jr. Los Pinos 567', 8, 8.50, true, 3, 3),
('Av. Arequipa 890', 15, 15.00, true, 4, 4),
('Calle Los Rosales 234', 6, 9.00, true, 5, 1),
('Av. El Sol 456', 12, 11.00, true, 6, 2),
('Jr. La Luna 789', 4, 7.50, false, 1, 3);

-- Datos para la tabla reserva con diferentes estados
-- Reservas completadas (pasadas)
INSERT INTO reserva (fecha_inicio, fecha_fin, estado, id_usuario, id_cochera) VALUES
('2025-03-01 10:00:00', '2025-03-01 12:00:00', 'completada', 1, 1),
('2025-03-02 14:00:00', '2025-03-02 16:00:00', 'completada', 2, 2),
('2025-03-10 09:00:00', '2025-03-10 11:00:00', 'completada', 3, 3),
('2025-03-15 13:00:00', '2025-03-15 15:00:00', 'completada', 4, 4);

-- Reservas pendientes (futuras)
INSERT INTO reserva (fecha_inicio, fecha_fin, estado, id_usuario, id_cochera) VALUES
('2025-04-20 10:00:00', '2025-04-20 12:00:00', 'pendiente', 1, 5),
('2025-04-21 15:00:00', '2025-04-21 17:00:00', 'pendiente', 2, 6),
('2025-04-22 08:00:00', '2025-04-22 10:00:00', 'pendiente', 3, 7),
('2025-04-25 14:00:00', '2025-04-25 16:00:00', 'pendiente', 4, 1),
('2025-04-28 11:00:00', '2025-04-28 13:00:00', 'pendiente', 5, 2);

-- Reservas canceladas
INSERT INTO reserva (fecha_inicio, fecha_fin, estado, id_usuario, id_cochera) VALUES
('2025-03-05 10:00:00', '2025-03-05 12:00:00', 'cancelada', 1, 3),
('2025-03-08 14:00:00', '2025-03-08 16:00:00', 'cancelada', 2, 4);

-- Reservas en curso (para el día actual)
INSERT INTO reserva (fecha_inicio, fecha_fin, estado, id_usuario, id_cochera) VALUES
('2025-04-09 08:00:00', '2025-04-09 18:00:00', 'en_curso', 3, 5),
('2025-04-09 09:00:00', '2025-04-09 17:00:00', 'en_curso', 4, 6);

-- Datos para la tabla pagos
-- Pagos por reservas completadas
INSERT INTO pagos (monto, fecha_pago, metodo_pago, id_usuario, id_dueno) VALUES
(25.00, '2025-03-01 12:15:00', 'tarjeta', 1, 1),
(20.00, '2025-03-02 16:10:00', 'efectivo', 2, 2),
(17.00, '2025-03-10 11:05:00', 'transferencia', 3, 3),
(30.00, '2025-03-15 15:20:00', 'tarjeta', 4, 4);

-- Pagos por adelantado para reservas pendientes
INSERT INTO pagos (monto, fecha_pago, metodo_pago, id_usuario, id_dueno) VALUES
(18.00, '2025-04-15 14:30:00', 'tarjeta', 1, 1),
(22.00, '2025-04-16 09:45:00', 'yape', 2, 2),
(15.00, '2025-04-17 10:20:00', 'plin', 3, 3);

-- Datos para la tabla calificacion
INSERT INTO calificacion (puntuacion, comentario, fecha, id_usuario, id_cochera) VALUES
(5, 'Excelente servicio, muy seguro', '2025-03-01 12:30:00', 1, 1),
(4, 'Buen servicio, pero un poco estrecho el espacio', '2025-03-02 16:30:00', 2, 2),
(5, 'Muy buena ubicación y seguridad', '2025-03-10 11:30:00', 3, 3),
(3, 'Servicio aceptable, podría mejorar la señalización', '2025-03-15 15:40:00', 4, 4);

-- Datos para la tabla registros_cochera
INSERT INTO registros_cochera (fecha_registro, detalles, id_cochera, id_dueno) VALUES
('2025-01-10 09:00:00', 'Registro inicial de cochera en Miraflores', 1, 1),
('2025-01-12 10:30:00', 'Registro de cochera familiar en San Isidro', 2, 2),
('2025-01-15 11:15:00', 'Registro de cochera comercial en Barranco', 3, 3),
('2025-01-20 14:00:00', 'Registro de cochera en edificio residencial en Surco', 4, 4),
('2025-01-25 15:30:00', 'Registro de cochera con seguridad 24/7 en San Borja', 5, 1),
('2025-02-01 09:45:00', 'Registro de cochera con techo en La Molina', 6, 2),
('2025-02-05 10:20:00', 'Registro de cochera con sistema automatizado en Miraflores', 7, 3);




--Testeamos
-- Ver todas las reservas pendientes
SELECT r.id_reserva, u.nombre AS usuario, c.direccion AS cochera, r.fecha_inicio, r.fecha_fin, r.estado
FROM reserva r
JOIN usuario u ON r.id_usuario = u.id_usuario
JOIN cochera c ON r.id_cochera = c.id_cochera
WHERE r.estado = 'pendiente'
ORDER BY r.fecha_inicio;

-- Ver todas las reservas completadas con sus pagos
SELECT r.id_reserva, u.nombre AS usuario, c.direccion AS cochera, r.fecha_inicio, r.fecha_fin, p.monto, p.metodo_pago
FROM reserva r
JOIN usuario u ON r.id_usuario = u.id_usuario
JOIN cochera c ON r.id_cochera = c.id_cochera
JOIN pagos p ON p.id_usuario = u.id_usuario AND p.id_dueno = c.id_dueno
WHERE r.estado = 'completada'
ORDER BY r.fecha_inicio;

-- Ver cocheras disponibles con sus distritos
SELECT c.id_cochera, c.direccion, c.capacidad, c.precio_hora, d.nombre AS distrito
FROM cochera c
JOIN distrito d ON c.id_distrito = d.id_distrito
WHERE c.disponible = true
ORDER BY c.precio_hora;

-- Ver calificaciones de cocheras
SELECT c.direccion AS cochera, d.nombre AS distrito, cal.puntuacion, cal.comentario, u.nombre AS usuario
FROM calificacion cal
JOIN cochera c ON cal.id_cochera = c.id_cochera
JOIN distrito d ON c.id_distrito = d.id_distrito
JOIN usuario u ON cal.id_usuario = u.id_usuario
ORDER BY cal.puntuacion DESC;