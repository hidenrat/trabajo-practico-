CREATE DATABASE IF NOT EXISTS sistema_reservas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sistema_reservas;

CREATE TABLE alojamientos (
    id_alojamiento INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    slug VARCHAR(150) NOT NULL UNIQUE,
    ubicacion_mapa TEXT NOT NULL,
    ubicacion TEXT NOT NULL,
    ubicacion_nombre VARCHAR(150) NOT NULL,
    precio_por_noche INT NOT NULL,
    capacidad INT NOT NULL,
    amenities TEXT NOT NULL,
    metros_cuadrados INT NOT NULL,
    baños INT NOT NULL,
    dormitorios INT NOT NULL,
    petFriendly BOOLEAN NOT NULL
);

CREATE TABLE reserva (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_alojamiento INT NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    cant_personas INT,
    total INT NOT NULL,
    nombre VARCHAR(150),
    email VARCHAR(150),
    telefono VARCHAR(100) NOT NULL,
    estado ENUM('pendiente','confirmada','cancelada') DEFAULT 'pendiente',
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_alojamiento) REFERENCES alojamientos(id_alojamiento)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE servicios_extras (
    id_servicio INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    subdesc TEXT NOT NULL,
    src VARCHAR(200) NOT NULL,
    capacidad INT NOT NULL,
    precio INT NOT NULL 
);

CREATE TABLE servicios_reserva (
    id_servicio_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_reserva INT NOT NULL,
    id_servicio INT NOT NULL,
    capacidad INT DEFAULT 1,

    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (id_servicio) REFERENCES servicios_extras(id_servicio)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE imagenes_alojamiento (
    id_imagen INT AUTO_INCREMENT PRIMARY KEY,
    id_alojamiento INT NOT NULL,
    src VARCHAR(255) NOT NULL,
    title VARCHAR(150) NOT NULL,
    subtitle VARCHAR(150) NOT NULL,
    FOREIGN KEY (id_alojamiento) REFERENCES alojamientos(id_alojamiento)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
