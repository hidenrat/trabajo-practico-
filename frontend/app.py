import os
from random import randint
from flask import Flask, flash, jsonify, redirect, url_for, render_template, request, session
import requests
import json
from flask_mail import Mail, Message

app = Flask(__name__)
# SECRET_KEY is required for sessions/flash to work. Prefer setting it via environment in production.
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key_change_me')

URL_BACKEND = "http://localhost:5003/api"

cabins = [
    {
        "name": "Mirador del Sol",
        "slug": "mirador-sol",
        "ubicacion": "Mendoza 315, Paraje Santas del Mar, Santa Teresita, Provincia de Buenos Aires, Argentina.",
        "ubicacion_nombre": "Camping Santas del Mar",
        "ubicacion_mapa": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3206.1200939936566!2d-56.69409702339975!3d-36.527096961606965!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x959c13b217a9e0c3%3A0xa3e02ff682c9495e!2sMendoza%20315%2C%20B7107%20Santa%20Teresita%2C%20Provincia%20de%20Buenos%20Aires!5e0!3m2!1ses-419!2sar!4v1763311568133!5m2!1ses-419!2sar",
        "images" :[
            {"src": "imgs/mirador-sol-1.jpg", "title": "Mirador del Sol", "subtitle": "Vista panorámica"},
            {"src": "/imgs/mirador-sol-2.jpg", "title": "Mirador del Sol", "subtitle": "Interior cálido"},
            {"src": "/imgs/mirador-sol-3.jpg", "title": "Mirador del Sol", "subtitle": "Terraza elevada"},
            {"src": "/imgs/mirador-sol-4.jpg", "title": "Mirador del Sol", "subtitle": "Piscina privada"},
            {"src": "/imgs/mirador-sol-5.jpg", "title": "Mirador del Sol", "subtitle": "Dormitorio principal"},
            {"src": "/imgs/mirador-sol-6.jpg", "title": "Mirador del Sol", "subtitle": "Dormitorio secundario"},
            {"src": "/imgs/mirador-sol-7.jpg", "title": "Mirador del Sol", "subtitle": "Baño moderno"},
            {"src": "/imgs/mirador-sol-8.jpg", "title": "Mirador del Sol", "subtitle": "Cocina equipada"}
        ],
        "precio_por_noche": 250,
        "capacidad": 4,
        "ammenities": "WiFi, Cocina, Piscina, Vista panorámica, Terraza elevada, Dormitorio principal, Dormitorio secundario, Baño moderno",
        "metros_cuadrados": 120,
        "baños": 2,
        "dormitorios": 2,
        "PetFriendly": True
    },
    {
        "name": "Bosque Vivo",
        "slug": "bosque-vivo",
        "ubicacion_mapa": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d25554.244290573894!2d-71.7442604347737!3d-36.811796947138724!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x966ec5f70bbb576b%3A0x717ebbf62152bfed!2sBosque%20Vivo!5e0!3m2!1ses!2sar!4v1763241520821!5m2!1ses!2sar",
        "ubicacion": "Camino a las Termas de Chillán, KM 2 Camino a Los Pellines Km. 2, 3880000 Pinto, Chile",
        "ubicacion_nombre": "Bosque Vivo",
        "images": [
            {"src": "/imgs/bosque-vivo-1.jpg", "title": "Bosque Vivo", "subtitle": "Rodeada de árboles"},
            {"src": "/imgs/bosque-vivo-2.jpg", "title": "Bosque Vivo", "subtitle": "Luz natural"},
            {"src": "/imgs/bosque-vivo-3.jpg", "title": "Bosque Vivo", "subtitle": "Patio acogedor"},
            {"src": "/imgs/bosque-vivo-4.jpg", "title": "Bosque Vivo", "subtitle": "Cocina rústica"},
            {"src": "/imgs/bosque-vivo-5.jpg", "title": "Bosque Vivo", "subtitle": "Dormitorio principal"},
            {"src": "/imgs/bosque-vivo-6.jpg", "title": "Bosque Vivo", "subtitle": "Baño rústico"}
        ],
        "precio_por_noche": 140,
        "capacidad": 3,
        "ammenities": "Cocina rústica, Patio acogedor, Dormitorio principal, Baño rústico, Rodeada de árboles, Luz natural",
        "metros_cuadrados": 90,
        "baños": 1,
        "dormitorios": 2,
        "PetFriendly": False
    },
    {
        "name": "Rincón Lunar",
        "slug": "rincon-lunar",
        "ubicacion_mapa": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3267.2918101606288!2d-57.53728665411472!3d-35.024429028768374!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x95a267bb9d4928c9%3A0x7f95e094db03db05!2sDescanso%20Atalaya!5e0!3m2!1ses!2sar!4v1763241962633!5m2!1ses!2sar",
        "ubicacion": "Calle 5 - Sta. Florentina, B1913 Atalaya, Provincia de Buenos Aires, Argentina.",
        "ubicacion_nombre": "Camping Descanso Atalaya",
        "images": [
            {"src": "/imgs/rincon-lunar-1.jpg", "title": "Rincón Lunar", "subtitle": "Cielo nocturno"},
            {"src": "/imgs/rincon-lunar-2.jpg", "title": "Rincón Lunar", "subtitle": "Interior acogedor"},
            {"src": "/imgs/rincon-lunar-3.jpg", "title": "Rincón Lunar", "subtitle": "Cocina moderna"},
            {"src": "/imgs/rincon-lunar-4.jpg", "title": "Rincón Lunar", "subtitle": "Dormitorio principal"},
            {"src": "/imgs/rincon-lunar-5.jpg", "title": "Rincón Lunar", "subtitle": "Baño elegante"},
            {"src": "/imgs/rincon-lunar-6.jpg", "title": "Rincón Lunar", "subtitle": "Piscina nocturna"}
        ],
        "precio_por_noche": 180,
        "capacidad": 2,
        "ammenities": "Cocina moderna, Dormitorio principal, Baño elegante, Piscina nocturna, Cielo nocturno, Interior acogedor",
        "metros_cuadrados": 70,
        "baños": 1,
        "dormitorios": 1,
        "PetFriendly": False
    },
    {
        "name": "Río Nativo",
        "ubicacion": "Av. Exequiel Bustillo 9491-8901, San Carlos de Bariloche, Río Negro",
        "ubicacion_mapa": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3005.867102109815!2d-71.41052892320393!3d-41.11559342986262!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x961a70c70bc95d5f%3A0x68aa96a9988d8ea0!2sAv.%20Exequiel%20Bustillo%209491-8901%2C%20San%20Carlos%20de%20Bariloche%2C%20R%C3%ADo%20Negro!5e0!3m2!1ses!2sar!4v1763319070882!5m2!1ses!2sar",
        "ubicacion_nombre": "Camping Lago Gutiérrez",
        "slug": "rio-nativo",
        "images": [
            {"src": "/imgs/rio-nativo-1.jpg", "title": "Río Nativo", "subtitle": "Junto al agua"},
            {"src": "/imgs/rio-nativo-2.jpg", "title": "Río Nativo", "subtitle": "Deck exterior"},
            {"src": "/imgs/rio-nativo-3.jpg", "title": "Río Nativo", "subtitle": "Interior cálido"},
            {"src": "/imgs/rio-nativo-4.jpg", "title": "Río Nativo", "subtitle": "Cocina rústica"},
            {"src": "/imgs/rio-nativo-5.jpg", "title": "Río Nativo", "subtitle": "Dormitorio principal"},
            {"src": "/imgs/rio-nativo-6.jpg", "title": "Río Nativo", "subtitle": "Baño principal"}
        ],
        "precio_por_noche": 100,
        "capacidad": 3,
        "ammenities": "Cocina rústica, Dormitorio principal, Baño principal, Deck exterior, Junto al agua, Interior cálido",
        "metros_cuadrados": 80,
        "baños": 1,
        "dormitorios": 1,
        "PetFriendly": True
    }
]


experiencias = [{
            "title": "Aventura en el bosque",
            "capacidad": 5,
            "subdesc": """Un circuito por los bosques que rodean las cabañas; compuesto por puentes flotantes y cascadas naturales a cada paso de la experiencia. 
            No te pierdas esta experiencia inolvidable. Alquilá tu cabaña Nordika.""",
            "src": "imgs/experiencia-1.jpg",
            "precio": 400
        },
        {
            "title": "Paseo natural",
            "capacidad": 6,
            "subdesc": """Un recorrido por senderos rodeados de flora nativa, con paradas en miradores naturales.
            Disfrutá de la tranquilidad y belleza del entorno. Alquilá tu cabaña Nordika.""",
            "src": "imgs/experiencia-2.jpg",
            "precio": 300
        },
        {
            "title": "Trekking por las montañas",
            "capacidad": 3,
            "subdesc": """Una experiencia de trekking que te llevará a través de paisajes montañosos impresionantes. 
            Conectá con la naturaleza y disfrutá de vistas inolvidables. Alquilá tu cabaña Nordika.""",
            "src": "imgs/experiencia-3.jpg",
            "precio": 650
        },
        {
            "title": "Meditación en el bosque",
            "capacidad": 3,
            "subdesc": """Una experiencia de mindfulness en medio del bosque, donde podrás conectarte con la naturaleza y disfrutar de un profundo momento de paz y tranquilidad. 
            Perfecta para relajarte y desconectar del estrés. Alquilá tu cabaña Nordika y vive la calma del bosque.""",
            "src": "imgs/experiencia-4.jpg",
            "precio": 160
        },
        {
            "title": "Paseo nocturno en el bosque",
            "capacidad": 4,
            "subdesc": """Vive la magia del bosque de noche, con una experiencia nocturna que te llevará a explorar los sonidos y las vistas bajo las estrellas. Escucha el crujir de las hojas y los murmullos del viento mientras te adentras en la oscuridad tranquila del bosque. 
            Una experiencia única para aquellos que buscan una conexión más profunda con la naturaleza. Alquilá tu cabaña Nordika y prepárate para una aventura bajo el cielo estrellado.""",
            "src": "imgs/experiencia-5.jpg",
            "precio": 220
        },
        {
            "title": "Paseo en barco por el río del bosque",
            "capacidad": 6,
            "subdesc": """Disfruta de un tranquilo paseo en barco o canoa por los ríos y lagos que rodean el bosque. Observa la fauna local y relájate mientras navegas entre los árboles, explorando paisajes inaccesibles por tierra. 
            Vive la serenidad del agua y la naturaleza. Alquilá tu cabaña Nordika y prepárate para una experiencia única en el bosque.""",
            "src": "imgs/experiencia-6.jpg",
            "precio": 700
        }
    ]


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
        return render_template('reservar_cabaña.html', cabin=cabin)
    else:
        # Redirigir a la página de reservar general si no encuentra la cabaña
        return redirect(url_for('cabañas'))

@app.route('/mis_reservas', methods=['GET', 'POST'])
def mis_reservas():
    if request.method == 'GET':
        return render_template('mis_reservas.html', datos=None)
    elif request.method == 'POST':
        id_reserva = request.form.get('reservation_id')
        response = requests.get(f"{http://localhost:5003/api}/reservas/{id_reserva}")
        if response.status_code == 200:
            datos_reserva = response.json()
        else:
            datos_reserva = False
        return render_template('mis_reservas.html', datos=datos_reserva)


@app.route('/cancelar', methods=['POST'])
def cancelar_reserva():
    id_reserva = request.form.get('reservation_id')
    print("ID recibido del formulario:", id_reserva)

    response = requests.post(f"{http://localhost:5003/api}/cancelar/{id_reserva}")
    
    if response.status_code == 200:
        flash('Reserva cancelada correctamente', 'success')
    else:
        flash('Hubo un error al cancelar la reserva', 'error')

    return redirect(url_for('mis_reservas', id=id_reserva))

@app.route('/datos_reserva')
def datos_reserva():
    datos = session.get('reservation')
    if not datos or not datos.get("check_in") or not datos.get("check_out") or not datos.get("cant_personas"):
        flash('Por favor, complete todos los campos de la reserva.', 'error')
        return redirect(url_for('reservar', cabin_slug=datos["cabin_slug"]))
    return render_template('ingreso_datos.html', datos=datos, cabañas=cabins, experiencias=experiencias)

@app.route('/procesar-reserva', methods=['POST'])
def procesar_reserva():
        # Guardo los datos del formulario de ingreso_datos.html
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        documento = request.form.get('documento')
        
        reservar_data = session.get('reservation')
        # En caso de que la session de reservar_cabaña.html no tenga información da error
        if not reservar_data:
            return "Error: No hay datos de reserva en sesión", 400
        # Guardo los datos de los dos formularios en un diccionario
        datos_reserva = {
            'cabin_slug': reservar_data['cabin_slug'],
            'nombre': nombre,
            'email': email,
            'telefono': telefono,
            'check_in': reservar_data['check_in'],
            'check_out': reservar_data['check_out'],
            'cant_personas': reservar_data['cant_personas'],
            'total': reservar_data['total']
        }
        # intento mandar el diccionario datos_reserva en formato json a una ruta llamada back-end/reserva
        try:
            response = requests.post(
                f"{'http://localhost:5003/api'}/reservas",
                json=datos_reserva,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                session.pop('reservation', None)
                return render_template('mis_reservas.html')
            else:
                error_data = response.json()
                return f"Error del backend: {error_data.get('error', 'Error desconocido')}", 400
        # Si no consigo mandarlo por problema del back-end devuelve error
        except requests.exceptions.RequestException as e:
            return f"Error de conexión con el backend: {str(e)}", 500
    
    return render_template('reservar_cabañas.html')

@app.route('/enviar_mail', methods=['POST'])
def enviar_mail():
    for cabaña in cabins:
        if cabaña['slug'] == request.form.get('cabin_slug'):
            cabaña_nombre = cabaña['name']
            break
    check_in = request.form.get('check_in')
    check_out = request.form.get('check_out')
    cant_personas = request.form.get('cant_personas')
    experiencias = request.form.getlist('experiencias')
    total = request.form.get('total')
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    telefono = request.form.get('telefono')
    id_reserva = randint(100000, 999999)  # Genera un ID de reserva aleatorio de 6 dígitos

    datos = {
        "id_reserva": id_reserva,
        "cabaña": cabaña_nombre,
        "check_in": check_in,
        "check_out": check_out,
        "cant_personas": cant_personas,
        "experiencias": experiencias,
        "total": total,
        "nombre": nombre,
        "email": email,
        "telefono": telefono
    }

    # Enviar datos al backend para crear la reserva
    #response = requests.post(f"{URL_BACKEND}/reservas/nueva", json=datos)
    #if response.status_code != 201:
    #    flash('Hubo un error al procesar la reserva. Por favor, intente nuevamente.', 'error')

    # Crear el mensaje de correo
    msg = Message('Confirmación de Reserva',
                  sender='practicotrabajo74@gmail.com',
                  recipients=[email])  # Correo del cliente

    # Renderizar el template HTML del correo
    msg.html = render_template('confirmacion_reserva_email.html',
                                cabin_slug=cabaña_nombre,
                                reserva_id=id_reserva,
                                check_in=check_in,
                                check_out=check_out,
                                cant_personas=cant_personas,
                                experiencias=experiencias,
                                total=total,
                                nombre=nombre,
                                email=email,
                                telefono=telefono)
    # Enviar el correo
    try:
        mail.send(msg)
    except Exception as e:
        print("Error al enviar el correo:", e)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port= 5002 , debug=True)
