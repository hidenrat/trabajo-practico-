USE sistema_reservas;

INSERT INTO alojamientos (
    name, slug, ubicacion_mapa, ubicacion, ubicacion_nombre,
    precio_por_noche, capacidad, amenities, metros_cuadrados,
    baños, dormitorios, petFriendly
) VALUES (
    'Mirador del Sol',
    'mirador-sol',
    'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3206.1200939936566!2d-56.69409702339975!3d-36.527096961606965!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x959c13b217a9e0c3%3A0xa3e02ff682c9495e!2sMendoza%20315%2C%20B7107%20Santa%20Teresita%2C%20Provincia%20de%20Buenos%20Aires!5e0!3m2!1ses-419!2sar!4v1763311568133!5m2!1ses-419!2sar',
    'Mendoza 315, Paraje Santas del Mar, Santa Teresita, Provincia de Buenos Aires, Argentina.',
    'Camping Santas del Mar',
    250,
    4,
    'WiFi, Cocina, Piscina, Vista panorámica, Terraza elevada, Dormitorio principal, Dormitorio secundario, Baño moderno',
    120,
    2,
    2,
    TRUE
),
(
    'Bosque Vivo',
    'bosque-vivo',
    'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3206.1200939936566!2d-56.69409702339975!3d-36.527096961606965!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x959c13b217a9e0c3%3A0xa3e02ff682c9495e!2sMendoza%20315%2C%20B7107%20Santa%20Teresita%2C%20Provincia%20de%20Buenos%20Aires!5e0!3m2!1ses-419!2sar!4v1763311568133!5m2!1ses-419!2sar',
    'Camino a las Termas de Chillán, KM 2 Camino a Los Pellines Km. 2, 3880000 Pinto, Chile',
    'Bosque Vivo',
    140,
    3,
    'Cocina rústica, Patio acogedor, Dormitorio principal, Baño rústico, Rodeada de árboles, Luz natural',
    90,
    1,
    2,
    FALSE
),
(
    'Rincón Lunar',
    'rincon-lunar',
    'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3267.2918101606288!2d-57.53728665411472!3d-35.024429028768374!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x95a267bb9d4928c9%3A0x7f95e094db03db05!2sDescanso%20Atalaya!5e0!3m2!1ses!2sar!4v1763241962633!5m2!1ses!2sar',
    'Calle 5 - Sta. Florentina, B1913 Atalaya, Provincia de Buenos Aires, Argentina.',
    'Camping Descanso Atalaya',
    180,
    2,
    'Cocina moderna, Dormitorio principal, Baño elegante, Piscina nocturna, Cielo nocturno, Interior acogedor',
    70,
    1,
    1,
    FALSE
),
(
    'Río Nativo',
    'rio-nativo',
    'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3005.867102109815!2d-71.41052892320393!3d-41.11559342986262!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x961a70c70bc95d5f%3A0x68aa96a9988d8ea0!2sAv.%20Exequiel%20Bustillo%209491-8901%2C%20San%20Carlos%20de%20Bariloche%2C%20R%C3%ADo%20Negro!5e0!3m2!1ses!2sar!4v1763319070882!5m2!1ses!2sar',
    'Av. Exequiel Bustillo 9491-8901, San Carlos de Bariloche, Río Negro',
    'Camping Lago Gutiérrez',
    100,
    3,
    'Cocina rústica, Dormitorio principal, Baño principal, Deck exterior, Junto al agua, Interior cálido',
    80,
    1,
    1,
    TRUE
);

INSERT INTO imagenes_alojamiento (
    id_alojamiento, src, title, subtitle
) VALUES (
    1,
    'imgs/mirador-sol-1.jpg',
    'Mirador del Sol',
    'Vista panorámica'
),
(
    1,
    'imgs/mirador-sol-2.jpg',
    'Mirador del Sol',
    'Interior cálido'
),
(
    1,
    'imgs/mirador-sol-3.jpg',
    'Mirador del Sol',
    'Terraza elevada'
),
(
    1,
    'imgs/mirador-sol-4.jpg',
    'Mirador del Sol',
    'Piscina privada'
),
(
    1,
    'imgs/mirador-sol-5.jpg',
    'Mirador del Sol',
    'Dormitorio principal'
),
(
    1,
    'imgs/mirador-sol-6.jpg',
    'Mirador del Sol',
    'Dormitorio secundario'
),
(
    1,
    'imgs/mirador-sol-7.jpg',
    'Mirador del Sol',
    'Baño moderno'
),
(
    1,
    'imgs/mirador-sol-8.jpg',
    'Mirador del Sol',
    'Cocina equipada'
),
(
    2,
    '/imgs/bosque-vivo-1.jpg',
    'Bosque Vivo',
    'Rodeada de árboles'
),
(
    2,
    '/imgs/bosque-vivo-2.jpg',
    'Bosque Vivo',
    'Luz natural'
),
(
    2,
    '/imgs/bosque-vivo-3.jpg',
    'Bosque Vivo',
    'Patio acogedor'
),
(
    2,
    '/imgs/bosque-vivo-4.jpg',
    'Bosque Vivo',
    'Cocina rústica'
),
(
    2,
    '/imgs/bosque-vivo-5.jpg',
    'Bosque Vivo',
    'Dormitorio principal'
),
(
    2,
    '/imgs/bosque-vivo-6.jpg',
    'Bosque Vivo',
    'Baño rústico'
),
(
    3,
    '/imgs/rincon-lunar-1.jpg',
    'Rincón Lunar',
    'Cielo nocturno'
),
(
    3,
    '/imgs/rincon-lunar-2.jpg',
    'Rincón Lunar',
    'Interior acogedor'
),
(
    3,
    '/imgs/rincon-lunar-3.jpg',
    'Rincón Lunar',
    'Cocina moderna'
),
(
    3,
    '/imgs/rincon-lunar-4.jpg',
    'Rincón Lunar',
    'Dormitorio principal'
),
(
    3,
    '/imgs/rincon-lunar-5.jpg',
    'Rincón Lunar',
    'Baño elegante'
),
(
    3,
    '/imgs/rincon-lunar-6.jpg',
    'Rincón Lunar',
    'Piscina nocturna'
),
(
    4,
    '/imgs/rio-nativo-1.jpg',
    'Río Nativo',
    'Junto al agua'
),
(
    4,
    '/imgs/rio-nativo-2.jpg',
    'Río Nativo',
    'Deck exterior'
),
(
    4,
    '/imgs/rio-nativo-3.jpg',
    'Río Nativo',
    'Interior cálido'
),
(
    4,
    '/imgs/rio-nativo-4.jpg',
    'Río Nativo',
    'Cocina rústica'
),
(
    4,
    '/imgs/rio-nativo-5.jpg',
    'Río Nativo',
    'Dormitorio principal'
),
(
    4,
    '/imgs/rio-nativo-6.jpg',
    'Río Nativo',
    'Baño principal'
);
INSERT INTO servicios_extras (title, capacidad, subdesc, src, precio) VALUES
("Aventura en el bosque", 
 5,
 "Un circuito por los bosques que rodean las cabañas; compuesto por puentes flotantes y cascadas naturales a cada paso de la experiencia. 
No te pierdas esta experiencia inolvidable. Alquilá tu cabaña Nordika.",
 "imgs/experiencia-1.jpg",
 400
),

("Paseo natural", 
 6,
 "Un recorrido por senderos rodeados de flora nativa, con paradas en miradores naturales.
Disfrutá de la tranquilidad y belleza del entorno. Alquilá tu cabaña Nordika.",
 "imgs/experiencia-2.jpg",
 300
),

("Trekking por las montañas", 
 3,
 "Una experiencia de trekking que te llevará a través de paisajes montañosos impresionantes. 
Conectá con la naturaleza y disfrutá de vistas inolvidables. Alquilá tu cabaña Nordika.",
 "imgs/experiencia-3.jpg",
 650
),

("Meditación en el bosque", 
 3,
 "Una experiencia de mindfulness en medio del bosque, donde podrás conectarte con la naturaleza y disfrutar de un profundo momento de paz y tranquilidad. 
Perfecta para relajarte y desconectar del estrés. Alquilá tu cabaña Nordika y vive la calma del bosque.",
 "imgs/experiencia-4.jpg",
 160
),

("Paseo nocturno en el bosque", 
 4,
 "Vive la magia del bosque de noche, con una experiencia nocturna que te llevará a explorar los sonidos y las vistas bajo las estrellas. Escucha el crujir de las hojas y los murmullos del viento mientras te adentras en la oscuridad tranquila del bosque. 
Una experiencia única para aquellos que buscan una conexión más profunda con la naturaleza. Alquilá tu cabaña Nordika y prepárate para una aventura bajo el cielo estrellado.",
 "imgs/experiencia-5.jpg",
 220
),

("Paseo en barco por el río del bosque", 
 6,
 "Disfruta de un tranquilo paseo en barco o canoa por los ríos y lagos que rodean el bosque. Observa la fauna local y relájate mientras navegas entre los árboles, explorando paisajes inaccesibles por tierra. 
Vive la serenidad del agua y la naturaleza. Alquilá tu cabaña Nordika y prepárate para una experiencia única en el bosque.",
 "imgs/experiencia-6.jpg",
 700
);
