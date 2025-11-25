from flask import Flask, jsonify, request
from flask_cors import CORS
from db import get_conexion 
from flask_mail import Mail, Message
import js, re
from daterime import date, datetime

#Se debe instalar Flask-CORS 
#para permitir llamadas desde el puerto 5002
#Comando en bash: pip install flask-cors
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_DEFAULT_SENDER'] = 'practicotrabajo74@gmail.com'
app.config['MAIL_USERNAME'] = 'practicotrabajo74@gmail.com'
app.config['MAIL_PASSWORD'] = 'vsug hlcz dpin dwvn'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
app = Flask(__name__)
CORS(app) 
#Habilitar CORS para permitir que el Frontend (puerto 5002) llame a este Backend (puerto 5003)

#ENDPOINT 

@app.route('/api/cabanas', methods=['GET']) # define un enpoint GET en la ruta /api/cabanas
def get_cabanas():
    conn = get_conexion() #crea la conexion con la base de datos
    cursor = conn.cursor(dictionary=True)# crea un cursor que retorna diccionarios

    #ejecuta una consulta SQL para obtener todos los alojamientos
    cursor.execute("""
        SELECT 
            id_alojamiento AS id,
            name,
            slug,
            ubicacion_mapa,
            ubicacion,
            ubicacion_nombre,
            precio_por_noche,
            capacidad,
            amenities,
            metros_cuadrados,
            baños,
            dormitorios,
            petFriendly
        FROM alojamientos;
    """)
    alojamientos = cursor.fetchall() #Recupera todos los resultados como una lista de diccionarios

    #ejecuta una consulta para obtener sus imágenes usando el id_alojamiento
    for alojamiento in alojamientos:
        cursor.execute("""
            SELECT src, title, subtitle
            FROM imagenes_alojamiento
            WHERE id_alojamiento = %s;
        """, (alojamiento['id'],))

        imagenes = cursor.fetchall()
        alojamiento['imagenes'] = imagenes #Agrega las imágenes al objeto alojamiento

    cursor.close()# cerras el cursor 
    conn.close()#cerras la conexion

    return jsonify(alojamientos)


@app.route('/api/servicios', methods=['GET'])
def obtener_servicio ():
    conn = get_conexion()  #crea la conexion con la base de datos   
    cursor = conn.cursor(dictionary=True) # crea uun cursor que devuelve diccionarios

    #obtiene los datos solicitados de la tabla servicios_extra
    cursor.execute("""
        SELECT 
             id_servicio,
            nombre AS title,
            capacidad,
            descripcion AS subdesc,
            src,
            precio
        FROM servicios_extras
    """)

    servicios = cursor.fetchall()#Recupera todos los resultados como una lista de diccionarios
    cursor.close()
    cunn.close()
    return jsonify(servicios), 200 

# En caso de que se quisiera obtener un alojamiento en particular
@app.route('/api/cabanas/<slug>', methods=['GET'])
def get_cabana(slug):
    conn = get_conexion() # crea la conexion con la base de datos
    cursor = conn.cursor(dictionary=True) # creamos un cursor que devuelve diccionarios

    # Obtener datos del alojamiento especifico
    cursor.execute("""
        SELECT 
            id_alojamiento AS id,
            name,
            slug,
            ubicacion_mapa,
            ubicacion,
            ubicacion_nombre,
            precio_por_noche,
            capacidad,
            amenities,
            metros_cuadrados,
            baños,
            dormitorios,
            petFriendly
        FROM alojamientos
        WHERE slug = %s;
    """, (slug,))

    alojamiento = cursor.fetchone() #obtiene una sola fila del resultado de la consulta SQL.

    if not alojamiento:
        cursor.close()
        conn.close()
        return jsonify({"error": "Alojamiento no encontrado"}), 404

    # Obtener imágenes de ese alojamiento especifico
    cursor.execute("""
        SELECT src, title, subtitle
        FROM imagenes_alojamiento
        WHERE id_alojamiento = %s;
    """, (alojamiento["id"],))

    imagenes = cursor.fetchall()
    alojamiento["imagenes"] = imagenes #agrega las imagenes al objeto alojamento

    cursor.close() # cierra el cursor
    conn.close() #cierra la conexion

    return jsonify(alojamiento), 200

def validar_fechas(check_in_str, check_out_str): # valida las fechas check_in, check_out
    check_in = datetime.strptime(check_in_str, "%Y-%m-%d").date()
    check_out = datetime.strptime(check_out_str, "%Y-%m-%d").date()

    if check_in >= check_out:
        raise ValueError("La fecha de entrada debe ser menor a la de salida") 
                                                                                #convierte los strings de fecha al objeto date
    if check_in < date.today():
        raise ValueError("La fecha de entrada no puede estar en el pasado")

    return check_in, check_out

def obtener_alojamiento_por_slug(slug):
    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_alojamiento, capacidad
        FROM alojamientos
        WHERE slug = %s
    """, (slug,))  # Busca el alojamiento por su slug

    fila = cursor.fetchone() #obtiene una sola fila del resultado

    cursor.close()
    conn.close()

    if not fila:
        raise ValueError("El alojamiento no existe")

    return fila 

def validar_capacidad(capacidad, num_personas): # verifica que el número de personas no exceda la capacidad máxima
    if num_personas > capacidad:
        raise ValueError(f"Capacidad excedida. Máximo permitido: {capacidad}")


def validar_email(email): #Define patrón regex para validar formato de email
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    
    if not re.match(patron, email):
        raise ValueError("El email ingresado no es válido.") #Si el email no coincide con el patrón, lanza error
    
    return email

def hay_superposicion(id_alojamiento, check_in, check_out): #Conexión a BD (cursor normal, sin diccionarios)
    conn = get_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) 
        FROM reserva 
        WHERE id_alojamiento = %s 
        AND estado != 'cancelada'
        AND (
            (check_in BETWEEN %s AND %s) OR
            (check_out BETWEEN %s AND %s) OR
            (%s BETWEEN check_in AND check_out) OR
            (%s BETWEEN check_in AND check_out)
        )
    """, (
        id_alojamiento,
        check_in, check_out,
        check_in, check_out,
        check_in, check_out
    )) #Busca reservas que se superpongan con las fechas solicitadas, Verifica 4 tipos de superposición posible

    cont = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return cont > 0

def insertar_reserva(id_alojamiento, data_form, check_in, check_out, email_valido):
    conn = get_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reserva 
        (id_alojamiento, check_in, check_out, cant_personas, 
        total, nombre, email, telefono, estado) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'confirmada')
    """, (
        id_alojamiento, check_in, check_out, data_form['cant_personas'], 
        data_form['total'], data_form['nombre'], email_valido, 
        data_form['telefono'])) #Inserta nueva reserva en la BD con estado "confirmada"

    conn.commit()
    id_reserva = cursor.lastrowid #Obtiene el ID auto-generado de la nueva reserva

    cursor.close()
    conn.close()

    return id_reserva

def insertar_servicio_reserva(id_reserva, id_servicio):
    conn = get_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO servicios_reserva (id_reserva, id_servicio)
        VALUES (%s, %s)
    """, (id_reserva, id_servicio)) #Inserta relación entre reserva y servicio extra

    conn.commit() #Confirma y cierra conexión
    cursor.close()
    conn.close()



@app.route('/api/reservas', methods=['POST'])
def crear_reserva():
    try:
        data_form = request.json

        # 1. Validar fechas
        check_in, check_out = validar_fechas(data_form['check_in'], data_form['check_out'])

        # 2. Obtener alojamiento y sus datos
        fila_alojamiento = obtener_alojamiento_por_slug(data_form['cabin_slug'])
        id_alojamiento = fila_alojamiento['id_alojamiento']
        capacidad = fila_alojamiento['capacidad']

        # 3. Validar capacidad
        validar_capacidad(capacidad, data_form['cant_personas'])

        # 4. Validar email
        email_valido = validar_email(data_form['email'])

        # 5. Validar superposición
        if hay_superposicion(id_alojamiento, check_in, check_out):
            return jsonify({
                "success": False,
                "error": "Las fechas seleccionadas no están disponibles"
            }), 400

        # 6. Insertar la reserva
        id_reserva = insertar_reserva(id_alojamiento, data_form, check_in, check_out, email_valido)

        #7. insertar servicio extra( si hay )
        experiencias = data_form.get("experiencias", []) 
        for exp in experiencias:
            insertar_servicio_reserva(id_reserva, exp) 
            

        return jsonify({
            "success": True,
            "message": "Reserva creada exitosamente",
            "id_reserva": id_reserva
        }), 201

    except ValueError as err:
        return jsonify({
            "success": False, 
            "error": str(err)}), 400

    except Exception as e:
        return jsonify({
            "success": False, 
            "error": f"Error del servidor: {e}"}), 500

# Obtener los detalles de una reserva específica
@app.route("/api/reservas/<int:id_reserva>", methods=["GET"])
def obtener_reserva(id_reserva):
    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            r.id_reserva,
            r.check_in,
            r.check_out,
            r.cant_personas,
            r.total,
            r.email,
            r.telefono,
            r.nombre,
            r.estado,
            r.fecha_reserva,
            a.name AS alojamiento,
            a.slug AS alojamiento_slug
        FROM reserva r
        JOIN alojamientos a
            ON r.id_alojamiento = a.id_alojamiento
        WHERE r.id_reserva = %s
    """, (id_reserva,))

    reserva = cursor.fetchone()

    cursor.close()
    conn.close()

    if not reserva:
        return jsonify({"error": "Reserva no encontrada"}), 404

    return jsonify(reserva), 200

@app.route('/api/reservas/<int:id_alojamiento>', methods=['GET']) #captura un entero desde la URL y lo pasa a la función como id_alojamiento
def obtener_reservas_alojamiento(id_alojamiento):

    conn = get_conexion()
    cursor = conn.cursor(dictionary=True) #hace que los resultados salgan como diccionario

    cursor.execute("""                             
        SELECT check_in, check_out 
        FROM reserva
        WHERE id_alojamiento = %s
          AND estado <> 'cancelada';
    """, (id_alojamiento,))    #Busca todas las reservas del alojamiento indicado. solo trae fecha_entrada y fecha_salida y filtra para no traer las canceladas

    reservas = cursor.fetchall() # lee todas las filas que devolvio el sql

    cursor.close()
    conn.close() # cierra el cursor y la conexion 

    # Convertimos al formato FullCalendar
    eventos = []
    for r in reservas:
        eventos.append({
            "title": "Reservado",
            "start": r["check_in"].strftime("%Y-%m-%d"),
            "end": r["check_out"].strftime("%Y-%m-%d"),
            "display": "block",
            "color": "#FF5252",
            "className": "reserved-event"
        })  # Convierte fecha_entrada y fecha_salida a texto con formato YYYY-MM-DD

    return jsonify(eventos)

@app.route('/api/reservas/cliente/<int:id_cliente>', methods=['GET']) #Registra la ruta /api/reservas/cliente/<id_cliente> como un endpoint GET en Flask.<int:id_cliente> captura un entero desde la URL y lo pasa como argumento id_cliente a la función.
def obtener_reservas_cliente(id_cliente):

    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            r.id_reserva,
            r.id_cliente,
            r.id_alojamiento,
            r.check_in,
            r.check_out,
            r.cant_personas,
            r.estado,
            r.total,
            r.nombre,
            r.email,
            r.telefono,
            r.fecha_reserva,
            a.nombre AS name,
            a.ubicacion
        FROM reserva r
        INNER JOIN alojamientos a ON r.id_alojamiento = a.id_alojamiento
        WHERE r.id_cliente = %s;
    """, (id_cliente,))  #Selecciona campos relevantes de la tabla reservas (alias r) y algunos campos del alojamiento (alias a).
                         #Hace un INNER JOIN para traer el nombre y direccion del alojamiento asociado a cada reserva. Filtra por r.id_cliente = %s. El %s es un placeholder y el segundo argumento (id_cliente,) pasa el valor de forma segura (previene inyección SQL).

    reservas = cursor.fetchall() #Recupera todas las filas resultantes de la consulta en una lista. Cada elemento es un diccionario con las columnas seleccionadas.

    cursor.close()
    conn.close()

    if not reservas: # verifica si la lista reservas este vacia ( no hay reservas para el cliente)
        return jsonify({"error": "No se encontraron reservas para este cliente"}), 404

    return jsonify(reservas) #Si hay reservas, devuelve la lista completa como JSON (HTTP 200 implícito). El JSON contendrá objetos con campos como id_reserva, fecha_entrada, fecha_salida, estado, nombre_alojamiento, etc.

@app.route('/api/reservas/enviar-mail/<int:id_reserva>', methods=['POST'])
def enviar_mail_reserva (id_reserva):
    conn = get_conexion ()
    cursor = conn.cursor (dictionary = true) 

    cursor.execute ("""
        SELECT
            r.id_reserva,
            r.nombre,
            r.check_in,
            r.check_out,
            r.cant_personas,
            r.total,
            r.email,
            r.telefono
            a.name as alojamiento
        FROM reserva r 
        INNER JOIN alojamintos a ON r.id_alojamientos = a.id_alojamiento
        WHERE r.id_reserva = %s;
    """ (id_reserva,))
    
    reserva = cursor.fetchone()
    cursor.close()
    conn.close()

    if not reserva:
        return jsonify({"error" : "reserva no encontrada" }) ,404

    asunto = f"confirmacion de su reserva #{id_reserva}"

    cuerpo_html =f"""
        <h2> Hola {reserva['nombre']}! </h2>
        <p> su reserva a sido confirmada </p>

        <h3> Datos sobre su reserva </h3>
        <ul>   
            <li><strong>Alojamiento:</strong> {reserva['alojamiento']}</li>
            <li><strong>Check-in:</strong> {reserva['check_in']}</li>
            <li><strong>Check-out:</strong> {reserva['check_out']}</li>
            <li><strong>Personas:</strong> {reserva['cant_personas']}</li>
            <li><strong>Total:</strong> ${reserva['total']}</li>
        </ul>
        <p>¡Gracias por elegirnos!</p>
    """
    
    msg = Message (asunto,recipients=[reserva["email"]])
    msg.html = cuerpo_html
    try:
        mail.send(msg)
    except Exception as e:
        return jsonify({"error": f"No se pudo enviar el mail: {str(e)}"}), 500

    return jsonify({"message": "Mail enviado correctamente"}), 200


@app.route('/api/reservas/cancelar/<int:id_reserva>', methods=['POST'])
def cancelar_reserva(id_reserva):

    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)

    # verificar que exista
    cursor.execute("""
        SELECT estado 
        FROM reserva 
        WHERE id_reserva = %s;
    """, (id_reserva,))  # Consulta la columna estado de la fila con id_reserva dado. Se usa placeholder %s para seguridad.
    
    reserva = cursor.fetchone() #devuelve el primer resultado o none si no hay nada

    if not reserva:
        cursor.close()
        conn.close() 
        return jsonify({"error": "Reserva no encontrada"}), 404
                            #si no encuentra nada se cierra el cursor y la conexion y devuelve "error" reserva no encontrada y ponemos un error 404
    
    # actualizar estado
    cursor.execute("""
        UPDATE reserva
        SET estado = 'cancelada'
        WHERE id_reserva = %s;
    """, (id_reserva,))   #usamos la sentencia UPDATE para modificar el estado a "cancelada" 
    
    conn.commit() #confirmamos el cambia a la base de datos, sin esto no se agregaria

    cursor.close()
    conn.close()

    return jsonify({"message": "Reserva cancelada correctamente"}), 200 #Devuelve un JSON con mensaje de confirmación y código HTTP 200 (OK).



if __name__ == '__main__':

    app.run(port=5003, debug=True)










