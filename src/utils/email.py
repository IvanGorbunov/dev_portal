from smtplib import SMTPAuthenticationError

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from rest_framework.exceptions import AuthenticationFailed

from settings import settings


def send_new_letter(email: str, theme: str, message: str):
    try:
        send_mail(
            theme,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
    except SMTPAuthenticationError:
        raise AuthenticationFailed()
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    except Exception as e:
        return f'Error: unable to send email due to {e}'
