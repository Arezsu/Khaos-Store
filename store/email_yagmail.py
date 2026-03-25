# store/email_yagmail.py
import yagmail
import os

def send_email_yagmail(to_email, subject, html_body, attachments=None):
    """
    Envío de email usando yagmail (una línea!)
    """
    try:
        # Configurar conexión
        yag = yagmail.SMTP(
            user=os.environ.get('EMAIL_HOST_USER'),
            password=os.environ.get('EMAIL_HOST_PASSWORD'),
            host=os.environ.get('EMAIL_HOST', 'smtp.gmail.com'),
            port=int(os.environ.get('EMAIL_PORT', 587)),
            smtp_starttls=True,
            smtp_ssl=False,
        )

        # Enviar email (una línea!)
        yag.send(
            to=to_email,
            subject=subject,
            contents=html_body,
            attachments=attachments,
        )

        print(f"✅ Email enviado a {to_email}")
        return True

    except Exception as e:
        print(f"❌ Error enviando email: {e}")
        return False

# Ejemplo ultra simplificado
def send_welcome_email_yagmail(user):
    yag = yagmail.SMTP(os.environ.get('EMAIL_HOST_USER'), os.environ.get('EMAIL_HOST_PASSWORD'))
    yag.send(
        to=user.email,
        subject="🎮 ¡Bienvenido a Khaos Store!",
        contents=f"""
        <h1>Hola {user.username}!</h1>
        <p>Tu cuenta ha sido creada exitosamente.</p>
        <a href="https://khaos-store.onrender.com">Comenzar a comprar</a>
        """,
    )
    return True