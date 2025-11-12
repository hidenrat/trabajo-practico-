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
reservas = [
        {"id": 1, "cabaña": "Mirador del Sol", "fecha_checkin": "2024-07-01", "fecha_checkout": "2024-07-05", "estado_reserva": "Confirmada"},
        {"id": 2, "cabaña": "Bosque Vivo", "fecha_checkin": "2024-08-10", "fecha_checkout": "2024-08-15", "estado_reserva": "Cancelada"},
    ]

@app.route('/reservas/<int:user_id>', methods=['GET'])
def get_reservas(user_id):
    match = False
    for reserva in reservas:
        if reserva["id"] == user_id:
            match = True
            return jsonify(reserva)
    if not match:
        return jsonify({"error": "Reserva no encontrada"}), 404


@app.route('/cancelar/<int:reserva_id>', methods=['POST'])
def cancelar_reserva(reserva_id):
    for reserva in reservas:
        if reserva["id"] == reserva_id:
            reserva["estado_reserva"] = "Cancelada"
            return jsonify({"message": "Reserva cancelada"}), 200
    return jsonify({"error": "Reserva no encontrada"}), 404

#Conexion entre front y back hecha, faltaría conectar con la base de datos MySQL

if __name__ == '__main__':
    app.run(port=5003, debug=True)