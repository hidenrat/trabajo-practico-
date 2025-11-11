from flask import Flask, jsonify
from flask_cors import CORS
from db import get_db_connection 
#Se debe instalar Flask-CORS 
#para permitir llamadas desde el puerto 5002
#Comando en bash: pip install flask-cors

app = Flask(__name__)
CORS(app) 
#Habilitar CORS para permitir que el Frontend (puerto 5002) llame a este Backend (puerto 5003)

#ENDPOINT 
@app.route('/api/cabanas', methods=['GET'])
def get_cabanas():
    conn = get_db_connection()      # Crea la conexión a MYSQL
    cursor = conn.cursor(dictionary=True)  # Crea un “cursor” para ejecutar consultas sql
    cursor.execute("""
        SELECT 
            id_alojamiento AS id,
            nombre,
            direccion,
            ciudad,
            pais,
            precio_noche,
            capacidad,
            descripcion
        FROM alojamientos;
    """)
    alojamientos = cursor.fetchall()  # Obtiene todos los resultados de la consulta
    cursor.close()                   # Cierra el cursor
    conn.close()                     # Cierra la conexión a la base de datos

    return jsonify(alojamientos)     # Devuelve los resultados como JSON

if __name__ == '__main__':
    app.run(port=5003, debug=True)