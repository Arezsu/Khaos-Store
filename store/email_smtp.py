# store/email_smtplib.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email_smtplib(to_email, subject, html_body):
    """
    Envío de email usando smtplib nativo
    """
    try:
        # Configuración desde variables de entorno
        smtp_server = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('EMAIL_PORT', 587))
        smtp_user = os.environ.get('EMAIL_HOST_USER')
        smtp_password = os.environ.get('EMAIL_HOST_PASSWORD')
        from_email = os.environ.get('DEFAULT_FROM_EMAIL', smtp_user)

        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        # Versión HTML
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)

        # Conectar y enviar
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # TLS para seguridad
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        print(f"✅ Email enviado a {to_email}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("❌ Error de autenticación. Verifica usuario/contraseña")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ Error SMTP: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

# Ejemplo de uso en views.py
def send_welcome_email(user):
    html_body = f"""
    <h1>Bienvenido a Khaos Store, {user.username}!</h1>
    <p>Tu cuenta ha sido creada exitosamente.</p>
    <a href="https://khaos-store.onrender.com">Comenzar a comprar</a>
    """
    return send_email_smtplib(user.email, "🎮 Bienvenido a Khaos Store", html_body)