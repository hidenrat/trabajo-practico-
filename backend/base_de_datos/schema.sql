CREATE DATABASE IF NOT EXISTS sistema_reservas;
USE sistema_reservas;

CREATE TABLE alojamientos (
    id_alojamiento INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    slug VARCHAR(150) NOT NULL,
    ubicacion VARCHAR(255) NOT NULL,
    ubicacion_nombre VARCHAR(150) NOT NULL,
    ubicacion_mapa VARCHAR(255) NOT NULL,
    images JASON NOT NULL, 
    precio_por_noche INT NOT NULL,
    capacidad INT NOT NULL,
    ammenities VARCHAR(255) NOT NULL
    ciudad VARCHAR(100),
    pais VARCHAR(100),
    metros_cuadrados INT NOT NULL,
    baños INT NOT NULL,
    dormitorios INT NOT NULL,
    petFriendly BOOLEAN,
);

CREATE TABLE reserva (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_alojamiento INT NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    cant_personas INT,
    total INT NOT NULL,
    nombre VARCHAR(150),
    email VARCHAR(150)
    telefono INT NOT NULL,
    estado ENUM('pendiente','confirmada','cancelada') DEFAULT 'pendiente',
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (id_alojamiento) REFERENCES alojamientos(id_alojamiento)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE servicios_extras (
    id_servicio INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio INT NOT NULL,
    capacidad INT NOT NULL,
);

CREATE TABLE servicios_reserva (
    id_servicio_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_reserva INT NOT NULL,
    id_servicio INT NOT NULL,
    cantidad INT DEFAULT 1,

    FOREIGN KEY (id_reserva) REFERENCES reservas(id_reserva)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (id_servicio) REFERENCES servicios_extras(id_servicio)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
