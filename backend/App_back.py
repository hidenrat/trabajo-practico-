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

if __name__ == '__main__':
    app.run(port=5003, debug=True)