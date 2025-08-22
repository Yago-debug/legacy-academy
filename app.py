from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
import re
import logging

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar logging
logging.basicConfig(
    filename='contacto.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'clave_secreta_segura')

# Configuración del correo desde variables de entorno
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 465))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

# Rutas
@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/alto-rendimiento')
def alto_rendimiento():
    return render_template('alto_rendimiento.html')

@app.route('/sobre-nosotros')
def sobre_nosotros():
    return render_template('sobre_nosotros.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/enviar_mensaje', methods=['POST'])
def enviar_mensaje():
    nombre = request.form.get('nombre', '').strip()
    email = request.form.get('email', '').strip()
    mensaje = request.form.get('mensaje', '').strip()

    logging.info(f"Formulario recibido - Nombre: {nombre}, Email: {email}")

    # Validaciones básicas
    if not nombre or not email or not mensaje:
        flash('Todos los campos son obligatorios.', 'error')
        logging.warning(f"Formulario incompleto - Nombre: {nombre}, Email: {email}, Mensaje: {mensaje}")
        return redirect(url_for('contacto'))

    # Validación de email
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        flash('El correo electrónico no es válido.', 'error')
        logging.warning(f"Correo inválido: {email}")
        return redirect(url_for('contacto'))

    # Intentar enviar el correo
    try:
        msg = Message(
            subject=f'Nuevo mensaje de {nombre} desde el formulario de contacto',
            recipients=['info@legacyacademymadrid.com'],
            body=f'Nombre: {nombre}\nEmail: {email}\n\nMensaje:\n{mensaje}'
        )
        mail.send(msg)
        logging.info(f"Correo enviado correctamente a info@legacyacademymadrid.com desde {email}")
        flash('Mensaje enviado correctamente. ¡Gracias por contactar con nosotros!', 'success')
        return redirect(url_for('contacto'))
    except Exception as e:
        logging.error(f"Error al enviar correo desde {email}: {e}")
        flash('Hubo un problema al enviar el mensaje. Intenta de nuevo más tarde.', 'error')
        return redirect(url_for('contacto'))

# Run
if __name__ == '__main__':
    app.run(debug=True)
