from flask import Flask, jsonify, render_template, request, redirect
from flask_cors import CORS
from db import get_conexion 
from flask_mail import Mail, Message
import re
from datetime import date, datetime, timedelta

# Crear la app primero
app = Flask(__name__, template_folder='templates')
CORS(app)

# Se debe instalar Flask-CORS para permitir llamadas desde el puerto 5002
# Comando en bash: pip install flask-cors

# Configuración de mail (ajustar usuario/clave en variables de entorno en producción)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_DEFAULT_SENDER'] = 'practicotrabajo74@gmail.com'
app.config['MAIL_USERNAME'] = 'practicotrabajo74@gmail.com'
app.config['MAIL_PASSWORD'] = 'vsug hlcz dpin dwvn'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
# Habilitar CORS para permitir que el Frontend (puerto 5002) llame a este Backend (puerto 5003)
URL_FRONT = "http://localhost:5002"
#ENDPOINT 

@app.route('/api/cabanas', methods=['GET'])
def get_cabanas():
    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)

    # Obtiene los alojamientos
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
    alojamientos = cursor.fetchall()

    # Recorre cada alojamiento para obtener sus imágenes
    for alojamiento in alojamientos:
        cursor.execute("""
            SELECT src, title, subtitle
            FROM imagenes_alojamiento
            WHERE id_alojamiento = %s;
        """, (alojamiento['id'],))

        imagenes = cursor.fetchall()
        alojamiento['imagenes'] = imagenes

    cursor.close()
    conn.close()

    return jsonify(alojamientos)

# Obtener los servicios de la tabla servicios_extra
@app.route('/api/servicios', methods=['GET'])
def obtener_servicio ():
    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            id_servicio,
            title,
            capacidad,
            subdesc,
            src,
            precio
        FROM servicios_extras
    """)

    servicios = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(servicios), 200 

# En caso de que se quisiera obtener un alojamiento en particular
@app.route('/api/cabanas/<slug>', methods=['GET'])
def get_solo_una_cabana(slug):
    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)

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

    alojamiento = cursor.fetchone()

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
    alojamiento["imagenes"] = imagenes

    cursor.close()
    conn.close()

    return jsonify(alojamiento), 200

def validar_fechas(check_in_str, check_out_str):
    check_in = datetime.strptime(check_in_str, "%Y-%m-%d").date()
    check_out = datetime.strptime(check_out_str, "%Y-%m-%d").date()

    if check_in >= check_out:
        raise ValueError("La fecha de entrada debe ser menor a la de salida")

    if check_in < date.today():
        raise ValueError("La fecha de entrada no puede estar en el pasado")

    return check_in, check_out

# Extrae el alojamiento según el slug de la URL
def obtener_alojamiento_por_slug(slug):
    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_alojamiento, capacidad
        FROM alojamientos
        WHERE slug = %s
    """, (slug,))

    fila = cursor.fetchone()

    cursor.close()
    conn.close()

    if not fila:
        raise ValueError("El alojamiento no existe")

    return fila 

def validar_capacidad(capacidad, num_personas):
    if num_personas > capacidad:
        raise ValueError(f"Capacidad excedida. Máximo permitido: {capacidad}")

def validar_email(email):
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    
    if not re.match(patron, email):
        raise ValueError("El email ingresado no es válido.")
    
    return email

def hay_superposicion(id_alojamiento, check_in, check_out):
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
    ))

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
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pendiente')
    """, (
        id_alojamiento, check_in, check_out, data_form['cant_personas'], 
        data_form['total'], data_form['nombre'], email_valido, 
        data_form['telefono']))

    conn.commit()
    id_reserva = cursor.lastrowid

    cursor.close()
    conn.close()

    return id_reserva


def send_mail_for_reserva(id_reserva):
    """Helper: obtiene datos de la reserva y envía el correo; lanza Exception si falla."""
    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            r.id_reserva,
            r.nombre,
            r.check_in,
            r.check_out,
            r.cant_personas,
            r.total,
            r.email,
            r.telefono,
            a.name AS alojamiento
        FROM reserva r
        INNER JOIN alojamientos a ON r.id_alojamiento = a.id_alojamiento
        WHERE r.id_reserva = %s
    """, (id_reserva,))

    reserva = cursor.fetchone()

    # obtener experiencias asociadas
    cursor.execute("""
        SELECT s.title, s.subdesc, s.precio
        FROM servicios_reserva sr
        JOIN servicios_extras s ON sr.id_servicio = s.id_servicio
        WHERE sr.id_reserva = %s
    """, (id_reserva,))
    experiencias_rows = cursor.fetchall()


    cursor.close()
    conn.close()

    if not reserva:
        raise ValueError("reserva no encontrada")

    experiencias_list = []
    for e in (experiencias_rows or []):
        experiencias_list.append({
            'title': e.get('title'),
            'subdesc': e.get('subdesc'),
            'precio': e.get('precio')
        })

    mis_reservas_url = f"{URL_FRONT}/mis_reservas?reserva_id={id_reserva}"

    msg = Message(
        'Confirmación de Reserva',
        sender=app.config.get('MAIL_DEFAULT_SENDER'),
        recipients=[reserva["email"]]
    )

    msg.html = render_template(
        'confirmacion_reserva_email.html',
        cabin_slug=reserva['alojamiento'],
        reserva_id=id_reserva,
        check_in=reserva['check_in'],
        check_out=reserva['check_out'],
        cant_personas=reserva['cant_personas'],
        experiencias=experiencias_list,
        total=reserva['total'],
        nombre=reserva['nombre'],
        email=reserva['email'],
        telefono=reserva['telefono'],
        mis_reservas_url=mis_reservas_url
    )

    mail.send(msg)


# Obtener los campos de una reserva específica
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
        print(f"No se encontró la reserva con id_reserva {id_reserva}")
        return jsonify({"error": "Reserva no encontrada"}), 404
    
    return jsonify(reserva), 200

# Se extraen los campos de la tabla reservas según el slug de la URL
def extraer_reservas_por_slug(slug):
    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_alojamiento
        FROM alojamientos
        WHERE slug = %s
    """, (slug,))

    fila = cursor.fetchone()
    id_alojamiento = fila["id_alojamiento"]

    cursor.execute("""
        SELECT check_in, check_out
        FROM reserva
        WHERE id_alojamiento = %s
        AND estado != 'cancelada'
        AND check_out >= CURDATE()
    """, (id_alojamiento,))

    reservas = cursor.fetchall()

    cursor.close()
    conn.close()

    for r in reservas:            
        r["check_in"] = r["check_in"].isoformat()
        r["check_out"] = r["check_out"] + timedelta(days=1)  # Ajuste para que la fecha de salida sea exclusiva
        r["check_out"] = r["check_out"].isoformat()

    return reservas

# Se encarga de enviar en formato json la información de la función extraer_reservas_por_slug
@app.route('/api/reservas/<slug>', methods=['GET'])
def retornar_reservas_por_slug(slug):
    try:
        reservas = extraer_reservas_por_slug(slug)

        return jsonify({
            "success": True,
            "reservas": reservas
        })

    except ValueError as err:
        return jsonify({
            "success": False,
            "error": str(err)
        }), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error del servidor: {e}"
        }), 500

# Se encarga de enviar los campos de la tabla de reserva de un id en específico y renderiza el tamplate de confirmacion_reserva_email
@app.route('/api/reservas/enviar-mail/<int:id_reserva>', methods=['POST'])
def enviar_mail_reserva(id_reserva):
    try:
        send_mail_for_reserva(id_reserva)
        return jsonify({"message": "Mail enviado correctamente"}), 200
    except ValueError:
        return jsonify({"error": "reserva no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": f"No se pudo enviar el email: {str(e)}"}), 500


@app.route('/api/reservas/<int:id_reserva>/experiencias', methods=['GET'])
def obtener_experiencias_reserva(id_reserva):
    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            sr.id_servicio,
            se.title,
            se.subdesc,
            se.src,
            se.capacidad,
            se.precio
        FROM servicios_reserva sr
        INNER JOIN servicios_extras se 
            ON sr.id_servicio = se.id_servicio
        WHERE sr.id_reserva = %s
    """, (id_reserva,))

    servicios = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(servicios), 200

@app.route('/api/reservas/cancelar/<int:id_reserva>', methods=['POST'])
def cancelar_reserva(id_reserva):

    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)

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


@app.route('/api/reservas/<int:id_reserva>/experiencias', methods=['GET', 'POST'])
def manejar_experiencias_reserva(id_reserva):
    """GET: devuelve lista de id_servicio asignados a la reserva
       POST: recibe JSON {"experiencias": [id_servicio, ...]} y reemplaza las relaciones
    """
    if request.method == 'GET':
        conn = get_conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT se.id_servicio, s.title, s.precio
            FROM servicios_reserva se
            JOIN servicios_extras s ON se.id_servicio = s.id_servicio
            WHERE se.id_reserva = %s
        """, (id_reserva,))
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        # devolver lista de ids y datos
        return jsonify([{"id_servicio": f['id_servicio'], "title": f['title'], "precio": f['precio']} for f in filas]), 200

    # POST -> actualizar
    payload = request.get_json() or {}
    nuevas = payload.get('experiencias')
    if nuevas is None:
        return jsonify({"error": "Se debe enviar la lista 'experiencias'"}), 400

    # validar que sea lista de enteros
    try:
        nuevas_ids = [int(x) for x in nuevas]
    except Exception:
        return jsonify({"error": "Formato inválido en 'experiencias'"}), 400

    conn = get_conexion()
    cursor = conn.cursor()
    try:
        # 1. Obtener servicios actuales
        cursor.execute("""
            SELECT id_servicio FROM servicios_reserva
            WHERE id_reserva = %s
        """, (id_reserva,))
        servicios_actuales = {row[0] for row in cursor.fetchall()}

        # Convert listas a sets
        servicios_nuevos = set(nuevas_ids)

        # 2. Determinar cuáles se agregan y cuáles se eliminan
        servicios_agregar = servicios_nuevos - servicios_actuales
        servicios_eliminar = servicios_actuales - servicios_nuevos

        # 3. AGREGAR nuevos servicios y sumar al total
        for id_servicio in servicios_agregar:
            # Insertar
            cursor.execute("""
                INSERT INTO servicios_reserva (id_reserva, id_servicio)
                VALUES (%s, %s)
            """, (id_reserva, id_servicio))

            # Sumar precio
            cursor.execute("""
                UPDATE reserva
                SET total = total + (
                    SELECT precio FROM servicios_extras WHERE id_servicio = %s
                )
                WHERE id_reserva = %s
            """, (id_servicio, id_reserva))

        # 4. ELIMINAR servicios quitados y restar del total
        for id_servicio in servicios_eliminar:
            # Eliminar
            cursor.execute("""
                DELETE FROM servicios_reserva
                WHERE id_reserva = %s AND id_servicio = %s
            """, (id_reserva, id_servicio))

            # Restar precio
            cursor.execute("""
                UPDATE reserva
                SET total = total - (
                    SELECT precio FROM servicios_extras WHERE id_servicio = %s
                )
                WHERE id_reserva = %s
            """, (id_servicio, id_reserva))
        conn.commit()
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({"error": f"Error actualizando experiencias: {str(e)}"}), 500

    cursor.close()
    conn.close()
    return jsonify({"message": "Experiencias actualizadas"}), 200


@app.route('/api/reservas', methods=['POST'])
def crear_reserva_con_experiencias():
    """Crea una reserva y asigna experiencias en una sola transacción, luego envía mail.
       JSON esperado: {
           cabin_slug, check_in, check_out, cant_personas, total, nombre, email, telefono, experiencias: [id,...]
       }
    """
    try:
        data_form = request.json or {}

        # validar campos mínimos
        required = ['cabin_slug', 'check_in', 'check_out', 'cant_personas', 'total', 'nombre', 'email', 'telefono']
        for r in required:
            if r not in data_form:
                return jsonify({"success": False, "error": f"Falta campo {r}"}), 400

        # 1. Validar fechas
        check_in, check_out = validar_fechas(data_form['check_in'], data_form['check_out'])

        # 2. Obtener alojamiento y sus datos
        fila_alojamiento = obtener_alojamiento_por_slug(data_form['cabin_slug'])
        id_alojamiento = fila_alojamiento['id_alojamiento']
        capacidad = fila_alojamiento['capacidad']

        # 3. Validar capacidad
        validar_capacidad(capacidad, int(data_form['cant_personas']))

        # 4. Validar email
        email_valido = validar_email(data_form['email'])

        # 5. Validar superposición
        if hay_superposicion(id_alojamiento, check_in, check_out):
            return jsonify({"success": False, "error": "Las fechas seleccionadas no están disponibles"}), 400

        experiencias_ids = data_form.get('experiencias') or []
        try:
            experiencias_ids = [int(x) for x in experiencias_ids]
        except Exception:
            return jsonify({"success": False, "error": "Formato inválido en 'experiencias'"}), 400

        # 6. Insertar reserva y experiencias en una sola conexión/tx
        conn = get_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO reserva
                (id_alojamiento, check_in, check_out, cant_personas, total, nombre, email, telefono, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pendiente')
            """, (
                id_alojamiento, check_in, check_out, data_form['cant_personas'], data_form['total'], data_form['nombre'], email_valido, data_form['telefono']
            ))
            id_reserva = cursor.lastrowid

            # insertar experiencias
            for sid in experiencias_ids:
                cursor.execute("INSERT INTO servicios_reserva (id_reserva, id_servicio) VALUES (%s, %s)", (id_reserva, sid))

            conn.commit()
        except Exception as e:
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"success": False, "error": f"Error creando reserva: {str(e)}"}), 500

        cursor.close()
        conn.close()

        # enviar mail (si falla, no revertimos la reserva - se registró)
        try:
            send_mail_for_reserva(id_reserva)
        except Exception:
            pass

        return jsonify({"success": True, "id_reserva": id_reserva}), 201

    except ValueError as err:
        return jsonify({"success": False, "error": str(err)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Error del servidor: {e}"}), 500

@app.route('/api/reservas/pagar/<int:id_reserva>', methods=['POST'])
def pagar_reserva(id_reserva):
    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        UPDATE reserva
        SET estado = 'confirmada'
        WHERE id_reserva = %s;
    """, (id_reserva,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Pago procesado correctamente"}), 200

if __name__ == '__main__':

    app.run(port=5003, debug=True)













