from flask import Flask, jsonify
from flask_cors import CORS
#Se debe instalar Flask-CORS 
#para permitir llamadas desde el puerto 5002
#Comando en bash: pip install flask-cors

app = Flask(__name__)
CORS(app) 
#Habilitar CORS para permitir que el Frontend (puerto 5002) llame a este Backend (puerto 5003)

#ENDPOINT 
@app.route('/api/cabanas', methods=['GET'])
def get_cabanas():
    #DATOS SIMULADOS, sin usar MySQL por ahora
    cabanas = [
        {"id": 1, "nombre": "Mirador del Sol", "tipo": "Familiar", "precio_noche": 150},
        {"id": 2, "nombre": "Bosque Vivo", "tipo": "Pareja", "precio_noche": 120},
        {"id": 3, "nombre": "Río Nativo", "tipo": "Lujo", "precio_noche": 200},
    ]
    
    return jsonify(cabanas)

#Datos simulados de reservas

@app.route('/api/reservas/cliente/<int:id_cliente>', methods=['GET']) #Registra la ruta /api/reservas/cliente/<id_cliente> como un endpoint GET en Flask.<int:id_cliente> captura un entero desde la URL y lo pasa como argumento id_cliente a la función.
def obtener_reservas_cliente(id_cliente):

    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            r.id_reserva,
            r.id_cliente,
            r.id_alojamiento,
            r.fecha_entrada,
            r.fecha_salida,
            r.num_personas,
            r.estado,
            r.fecha_reserva,
            a.nombre AS nombre_alojamiento,
            a.direccion
        FROM reservas r
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
        FROM reservas 
        WHERE id_reserva = %s;
    """, (id_reserva,))  # Consulta la columna estado de la fila con id_reserva dado. Se usa placeholder %s para seguridad.
    
    reserva = cursor.fetchone() #devuelve el primer resultado o none si no hay nada

    if not reserva:
        cursor.close()
        conn.closey 
        return jsonify({"error": "Reserva no encontrada"}), 404
                            #si no encuentra nada se cierra el cursor y la conexion y devuelve "error" reserva no encontrada y ponemos un error 404
    
    # actualizar estado
    cursor.execute("""
        UPDATE reservas
        SET estado = 'cancelada'
        WHERE id_reserva = %s;
    """, (id_reserva,))   #usamos la sentencia UPDATE para modificar el estado a "cancelada" 
    
    conn.commit() #confirmamos el cambia a la base de datos, sin esto no se agregaria

    cursor.close()
    conn.close()

    return jsonify({"message": "Reserva cancelada correctamente"}), 200 #Devuelve un JSON con mensaje de confirmación y código HTTP 200 (OK).


# Crear reserva
@app.route('/api/reservas/nueva', methods=['POST'])
def crear_reserva():
    pass  # Implementar la lógica para crear una nueva reserva

# Obtener las fechas reservadas segun la cabaña
@app.route('/api/reservas/fechas/<int:id_alojamiento>', methods=['GET'])

def obtener_fechas_reservadas(cabaña):
    pass  # Implementar la lógica para obtener las fechas reservadas

if __name__ == '__main__':

    app.run(port=5003, debug=True)
