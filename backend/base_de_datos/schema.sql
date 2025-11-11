CREATE DATABASE IF NOT EXISTS sistema_reservas;
USE sistema_reservas;

CREATE TABLE alojamientos (
    id_alojamiento INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    ciudad VARCHAR(100),
    pais VARCHAR(100),
    precio_noche DECIMAL(10,2) NOT NULL,
    capacidad INT,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_alojamiento INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    telefono VARCHAR(20),
    fecha_entrada DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    num_personas INT,
    estado ENUM('pendiente','confirmada','cancelada') DEFAULT 'pendiente',
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_alojamiento) REFERENCES alojamientos(id_alojamiento)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);