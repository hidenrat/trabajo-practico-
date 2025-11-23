from datetime import datetime
import os
from random import randint
from flask import Flask, flash, jsonify, redirect, url_for, render_template, request, session
import requests



app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key_change_me')

URL_BACKEND = "http://localhost:5003"

cabins = requests.get(f"{URL_BACKEND}/api/cabanas").json()
experiencias = requests.get(f"{URL_BACKEND}/api/servicios").json()

@app.route('/')
def index():
    comentarios = [{
    "name": "Elena Márquez",
    "src": "imgs/avatar-1.jpg",
    "info": "Viajera y fotógrafa de naturaleza.",
    "opinion": "La experiencia fue increíblemente relajante. Las cabañas combinan un diseño moderno con un ambiente cálido y acogedor que te hace sentir como en casa desde el primer momento. Me encantó la atención al detalle: desde la iluminación suave hasta los materiales naturales usados en la decoración. Además, el silencio del entorno y el sonido del viento entre los árboles crean una atmósfera perfecta para desconectar. Es ideal tanto para una escapada romántica como para unos días de descanso en soledad."
},
{
    "name": "Carlos Ibáñez",
    "src": "imgs/avatar.jpg",
    "info": "Arquitecto.",
    "opinion": "Lo que más me impresionó fue la arquitectura de las cabañas: líneas minimalistas, ventanales amplios y un uso inteligente de la madera que resalta el entorno natural sin invadirlo. Se nota una clara inspiración escandinava, con un equilibrio entre funcionalidad y calidez. El aislamiento térmico es excelente, y disfrutar del paisaje nevado desde el interior fue una experiencia mágica. Sin duda, un modelo de alojamiento que demuestra que el confort moderno puede ir de la mano con la sostenibilidad."
},
{
    "name": "Lucas Torres",
    "src": "imgs/avatar-2.jpg",
    "info": "Periodista de viajes.",
    "opinion": "Nordika Cabins ofrece una experiencia distinta, pensada para quienes buscan desconexión total sin renunciar al confort. Las cabañas están equipadas con todo lo necesario, pero lo que realmente marca la diferencia es el ambiente: paz, diseño y naturaleza se mezclan de forma perfecta. El servicio fue amable y discreto, y los alrededores invitan a caminar, leer o simplemente contemplar el paisaje. Es un lugar que invita a bajar el ritmo y disfrutar del presente."
}
]
    return render_template('index.html', cabins=cabins, experiences=experiencias, testimonials=comentarios)

@app.route('/cabañas')
def cabañas():
    return render_template('nuestras_cabañas.html', cabins=cabins)
                           
@app.route('/reservar/<cabin_slug>', methods=['GET', 'POST'])
def reservar_cabaña(cabin_slug):
    if request.method == 'POST':
        check_in = request.form.get('check_in')
        check_out = request.form.get('check_out')
        cant_personas = request.form.get('guests')
        total = request.form.get('total')

        session['reservation'] = {
            'cabin_slug': cabin_slug,
            'check_in': check_in,
            'check_out': check_out,
            'cant_personas': int(cant_personas),
            'total': int(total)
        }
        return redirect(url_for('datos_reserva'))

    cabin = next((c for c in cabins if c['slug'] == cabin_slug), None)
    if cabin:
        datos_reservas = requests.get(f"{URL_BACKEND}/api/reservas/{cabin['slug']}").json()
        fechas = datos_reservas.get('reservas', [])
        print(fechas)
        return render_template('reservar_cabaña.html', cabin=cabin, real_reserved_dates=fechas)
    else:
        # Redirigir a la página de reservar general si no encuentra la cabaña
        return redirect(url_for('cabañas'))

@app.route('/mis_reservas', methods=['GET', 'POST'])
def mis_reservas():
    if request.method == 'GET':
        return render_template('mis_reservas.html', datos=None)
    elif request.method == 'POST':
        id_reserva = request.form.get('reservation_id')
        response = requests.get(f"{URL_BACKEND}/api/reservas/{id_reserva}")
        if response.status_code == 200:
            datos_reserva = response.json()
        else:
            datos_reserva = False
        print(datos_reserva)
        datos_reserva["check_in"] = datetime.strptime(datos_reserva["check_in"], "%a, %d %b %Y %H:%M:%S GMT").date()
        datos_reserva["check_out"] = datetime.strptime(datos_reserva["check_out"], "%a, %d %b %Y %H:%M:%S GMT").date()

        cantidad_noches = (datos_reserva["check_out"] - datos_reserva["check_in"]).days
        datos_reserva["cantidad_noches"] = cantidad_noches
        return render_template('mis_reservas.html', datos=datos_reserva)

@app.route('/cancelar_reserva', methods=['POST'])
def cancelar_reserva():
    id_reserva = request.form.get('reservation_id')
    response = requests.post(f"{URL_BACKEND}/api/reservas/cancelar/{id_reserva}")
    if response.status_code == 200:
        flash('Reserva cancelada con éxito.', 'success')
    else:
        flash('Error al cancelar la reserva.', 'error')
    return redirect(url_for('mis_reservas'))

@app.route('/datos_reserva')
def datos_reserva():
    datos = session.get('reservation')
    if not datos or not datos.get("check_in") or not datos.get("check_out") or not datos.get("cant_personas"):
        flash('Por favor, complete todos los campos de la reserva.', 'error')
        return redirect(url_for('reservar', cabin_slug=datos["cabin_slug"]))
    return render_template('ingreso_datos.html', datos=datos, cabañas=cabins, experiencias=experiencias)

@app.route('/procesar_reserva', methods=['POST'])
def procesar_reserva():
        # Guardo los datos del formulario de ingreso_datos.html
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        documento = request.form.get('documento')
        
        reservar_data = session.get('reservation')

        if not reservar_data:
            return "Error: No hay datos de reserva en sesión", 400
        # Guardo los datos de los dos formularios en un diccionario
        experiencias_seleccionadas = request.form.getlist("experiencias")
        datos_reserva = {
            'cabin_slug': reservar_data['cabin_slug'],
            'nombre': nombre,
            'email': email,
            'telefono': telefono,
            'check_in': reservar_data['check_in'],
            'check_out': reservar_data['check_out'],
            'cant_personas': reservar_data['cant_personas'],
            'total': reservar_data['total'],
            'experiencias': experiencias_seleccionadas
        }
    
        try:
            response = requests.post(
                f"{URL_BACKEND}/api/reservas",
                json=datos_reserva,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                session.pop('reservation', None)
                reserva_id = response.json().get("id_reserva")

                return render_template('confirmacion_reserva_email.html', reserva_id=reserva_id, email=email, telefono=telefono, cabin_slug=datos_reserva['cabin_slug'], check_in=datos_reserva['check_in'], check_out=datos_reserva['check_out'], cant_personas=datos_reserva['cant_personas'], total=datos_reserva['total'], experiencias=experiencias, nombre=nombre)
            else:
                error_data = response.json()
                return f"Error del backend: {error_data.get('error', 'Error desconocido')}", 400
        # Si no consigo mandarlo por problema del back-end devuelve error
        except requests.exceptions.RequestException as e:
            return f"Error de conexión con el backend: {str(e)}", 500

@app.route('/pagar_reserva', methods=['POST'])
def pagar_reserva():
    id_reserva = request.form.get('reservation_id')
    # Aquí iría la lógica de pago, que puede incluir redireccionar a una pasarela de pago
    # Por ahora, simplemente simulamos el pago exitoso
    response = requests.post(f"{URL_BACKEND}/api/reservas/pagar/{id_reserva}")
    if response.status_code == 200:
        flash('Reserva pagada con éxito.', 'success')
    else:
        flash('Error al procesar el pago.', 'error')
    return redirect(url_for('mis_reservas'))

if __name__ == '__main__':
    app.run(port= 5002 , debug=True)
