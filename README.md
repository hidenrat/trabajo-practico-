**antes de iniciarse el proyecto en flask debe/n instalarse**
- flask_mail --> pip install flask_mail
- requests --> pip install requests
- flask-cors --> pip install flask-cors

**Comentario: para iniciar las paginas se debe inicializar el archivo "iniciar_pagina.sh"**

---
# Base de datos:
La base de datos está diseñada siguiendo principios de normalización, permitiendo que un cliente pueda realizar múltiples reservas, gestionar servicios adicionales, y mantener un historial ordenado y seguro. Consta de cuatro tablas principales:
1. **alojamientos**
Contiene toda la información de las cabañas disponibles en el sistema. Esta información se usa en el frontend para mostrar la información de cada alojamiento y también su disponibilidad. El campo slug, ayuda al endpoint get_cabana para saber a cual es la cabaña a la que se le está haciendo la reserva
2. **reservas**
Registra cada reserva hecha por los clientes.
3. **servicios_extras**
Catálogo de servicios adicionales que se pueden ofrecer.
4. **servicios_reserva**
Tabla intermedia que conecta reservas con servicios extras.
5. **imagenes_alojamiento**
Contiene el src de las imagenes sus titulos y subtitulos de cada uno de los alojamiento. Luego estos serán usados en el frontend de la página.
6. **opiniones**
Contiene el nombre del usuario, su imágen y la opinión del usuario respecto a su estadía y los servicios extra utilizados, además de las valoraciónes del usuario respecto a los mismos.

En valores_iniciales.sql están los valores iniciales que se le agregan a las tablas creadas en schema.sql, se agregan a las tablas alojamientos, imagenes_alojamientos.

# Endpoints del Backend:
**En db.py :** Se crea la funcion get_conexion para configurar la conexión con la base de datos utilizando la librería mysql.connector, luego esta función se importara en app-back.py y se usará cada vez que se requiera ejecutar una consulta a base de datos a traves del método cursor

**En App_back.py :** 
1. **api/cabanas:** a través de la funcion get_cabanas, primero obtiene todos los campos de la tabla alojamientos y luego para cada alojamiento obtiene las imagenes, titulos y subtitulos asociados. Luego los pasa a formato json para que los reciba el frontend y los devuelve.
2. **api/cabanas/<slug>:** a traves de la funcion get_cabana(slug) hace algo analogo a la funcion get_cabanas pero esta vez solamente para los valores asociados a un alojamiento, el alojamiento que está relacionado al slug que obtiene por parámetro.
3. **api/servicios:** a traves de la función obtener_servicio se obtienen todos los campos de la tabla servicios. Luego los pasa a formato json para que los reciba el frontend y los devuelve, también se devuelve código 200 para indicar que se obtuvieron los valores y se pasaron satisfactoriamente.
4. **api/reservas:** a traves de la función crear_reserva, primero se validan los datos para ver que se esté realizando la reserva en una fecha válida, luego se obtienen el id_alojamiento y la capacidad del alojamiento usando su slug como parámetro, luego se valida que se haya ingresado una capacidad de huespedes válida, luego se valida que el formato del mail sea valido y luego se valida que la cabaña esté disponible en las fechas elegidas. Habiendo confirmado todo este se ingresa la reserva en la tabla reservas y luego en el caso de haberse seleccionado un servicio extra se inserta este servicio extra en la tabla servicio_reserva
5. **/api/reservas/<int:id_reserva>:** a traves de la funcion obtener_reserva que recibe como parametro el id_reserva usa este parámetro para obtener los valores de la tabla reservas asociados a ese id_reserva, en caso de no existir devuelve error 404, y en caso de existir los pasa a formato json para poder ser usado por el frontend y los devuelve.
6. **/api/reservas/<id_alojamiento>:** a traves de la función obtener_reservas_alojamiento que recibe un id_alojamiento como parametro, busca en la base de datos todas las reservas de ese alojamiento que no estén canceladas, toma sus fechas de entrada y salida, convierte esas fechas al formato YYYY-MM-DD y devuelve una lista de eventos en formato JSON lista para ser usada por FullCalendar.
7. **/api/reservas/enviar-mail/<int:id_reserva>:** a traves de la función enviar_mail_reserva que recibe un id_reserva como parametro busca en la tabla reservas la reserva asociada a ese id_reserva, si no lo encuentra devuelve error 404, con los datos de esa reserva y haciendo uso de la librería flask_mail los envía al usuario 
8. **/api/reservas/cancelar/<int:id_reserva>:** a traves de la funcion cancelar_reserva que recibe id_reserva como parametro, va a buscar en la tabla reservas de la base de datos, en caso de no encontrarla va a devolver error 404. Pero habiendola encontrado va a cambiar el estado de dicha reserva a "cancelada", luego devuelve un mensaje con código 200 indicando que se canceló la reserva satisfactoriamente
9. **/api/reservas/cliente/<int:id_cliente>:** <mark>Por el momento no se encuentra en uso pero en caso de ser necesaria podría usarse, tampoco existen los campos de cliente en la base de datos ni hay una tabla donde se guarden los clientes de la base de datos, en caso de usarse eventualmente se agrega su explicación</mark> a traves de la función obtener_reservas_cliente va a obtener valores asociados a ese cliente en ambas tablas reservas y alojamientos y luego los devuelve en formato json para ser usados por el frontend
