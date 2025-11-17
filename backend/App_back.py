from flask import Flask, jsonify
from flask_cors import CORS
from db import get_conexion 
#Se debe instalar Flask-CORS 
#para permitir llamadas desde el puerto 5002
#Comando en bash: pip install flask-cors

app = Flask(__name__)
CORS(app) 
#Habilitar CORS para permitir que el Frontend (puerto 5002) llame a este Backend (puerto 5003)

#ENDPOINT 
@app.route('/api/cabanas', methods=['GET'])
def get_cabanas():
    conn = get_conexion()      # Crea la conexión a MYSQL
    cursor = conn.cursor(dictionary=True)  # Crea un “cursor” para ejecutar consultas sql
    cursor.execute("""
        SELECT 
            id_alojamiento AS id,
            name,
            ubicacion,
            ciudad,
            pais,
            precio_por_noche,
            capacidad,
            ammenities,
            slug,
            ubicacion_nombre,
            ubicacion_mapa,
            images,
            metros_cuadrados,
            baños,
            dormitorios,
            petFriendly
        FROM alojamientos;
    """)
    alojamientos = cursor.fetchall()  # Obtiene todos los resultados de la consulta
    cursor.close()                   # Cierra el cursor
    conn.close()                     # Cierra la conexión a la base de datos

    return jsonify(alojamientos)     # Devuelve los resultados como JSON

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




