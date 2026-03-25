# store/email_django.py
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
import os

def send_email_django(to_email, subject, html_body, text_body=None):
    """
    Envío de email usando django.core.mail
    """
    try:
        if text_body is None:
            text_body = "Versión en texto plano del email"

        # Opción 1: send_mail simple
        send_mail(
            subject=subject,
            message=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            html_message=html_body,
            fail_silently=False,
        )

        # Opción 2: EmailMultiAlternatives (más potente)
        # email = EmailMultiAlternatives(
        #     subject=subject,
        #     body=text_body,
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     to=[to_email],
        # )
        # email.attach_alternative(html_body, "text/html")
        # email.send()

        print(f"✅ Email enviado a {to_email}")
        return True

    except Exception as e:
        print(f"❌ Error enviando email: {e}")
        return False

# Usando templates HTML (mejor práctica)
def send_welcome_email_django(user):
    context = {
        'username': user.username,
        'email': user.email,
    }
    html_body = render_to_string('store/emails/welcome.html', context)
    return send_email_django(
        user.email,
        "🎮 ¡Bienvenido a Khaos Store!",
        html_body
    )