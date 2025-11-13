import os
from flask import Flask, flash, jsonify, redirect, url_for, render_template, request, session
import requests
from flask_mail import Mail, Message

app = Flask(__name__)
# SECRET_KEY is required for sessions/flash to work. Prefer setting it via environment in production.
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key_change_me')

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_DEFAULT_SENDER'] = 'practicotrabajo74@gmail.com'
app.config['MAIL_USERNAME'] = 'practicotrabajo74@gmail.com'
app.config['MAIL_PASSWORD'] = 'vsug hlcz dpin dwvn'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail= Mail(app)

URL_BACKEND = "http://localhost:5003"

cabins = [
    {
        "name": "Mirador del Sol",
        "slug": "mirador-sol",
        "images": [
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
        "ammenities": "WiFi, Cocina, Piscina, Vista panorámica, Terraza elevada, Dormitorio principal, Dormitorio secundario, Baño moderno"
    },
    {
        "name": "Bosque Vivo",
        "slug": "bosque-vivo",
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
        "ammenities": "Cocina rústica, Patio acogedor, Dormitorio principal, Baño rústico, Rodeada de árboles, Luz natural"
    },
    {
        "name": "Rincón Lunar",
        "slug": "rincon-lunar",
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
        "ammenities": "Cocina moderna, Dormitorio principal, Baño elegante, Piscina nocturna, Cielo nocturno, Interior acogedor"
    },
    {
        "name": "Río Nativo",
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
        "ammenities": "Cocina rústica, Dormitorio principal, Baño principal, Deck exterior, Junto al agua, Interior cálido"
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
        return redirect(url_for('reservar'))

@app.route('/mis_reservas', methods=['GET', 'POST'])
def mis_reservas():
    if request.method == 'GET':
        return render_template('mis_reservas.html', datos=None)
    elif request.method == 'POST':
        id_reserva = request.form.get('reservation_id')
        response = requests.get(f"{URL_BACKEND}/reservas/{id_reserva}")
        if response.status_code == 200:
            datos_reserva = response.json()
        else:
            datos_reserva = False
        return render_template('mis_reservas.html', datos=datos_reserva)


@app.route('/cancelar', methods=['POST'])
def cancelar_reserva():
    id_reserva = request.form.get('reservation_id')
    print("ID recibido del formulario:", id_reserva)

    response = requests.post(f"{URL_BACKEND}/cancelar/{id_reserva}")
    
    if response.status_code == 200:
        flash('Reserva cancelada correctamente', 'success')
    else:
        flash('Hubo un error al cancelar la reserva', 'error')

    return redirect(url_for('mis_reservas', id=id_reserva))

@app.route('/datos_reserva', methods=['GET', 'POST'])
def datos_reserva():
    if request.method == 'POST':
        # Enviar datos al backend a implementar
        return redirect(url_for('index'))
    datos = session.get('reservation')
    if not datos or not datos.get("check_in") or not datos.get("check_out") or not datos.get("cant_personas"):
        flash('Por favor, complete todos los campos de la reserva.', 'error')
        return redirect(url_for('reservar', cabin_slug=datos["cabin_slug"]))
    return render_template('ingreso_datos.html', datos=datos, cabañas=cabins, experiencias=experiencias)

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

    # Crear el mensaje de correo
    msg = Message('Confirmación de Reserva',
                  sender='practicotrabajo74@gmail.com',
                  recipients=[email])  # Correo del cliente

    # Renderizar el template HTML del correo
    msg.html = render_template('confirmacion_reserva_email.html',
                               cabin_slug=cabaña_nombre,
                               check_in=check_in,
                               check_out=check_out,
                               cant_personas=cant_personas,
                               experiencias=experiencias,
                               total=total,
                               nombre=nombre,
                               email=email,
                               telefono=telefono)

    try:
        mail.send(msg)
    except Exception as e:
        print("Error al enviar el correo:", e)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port= 5002 , debug=True)