from datetime import datetime

from django.utils.translation import gettext_lazy as _

from .tasks import send_new_email
from utils.email import send_new_letter

from settings import settings
from ..users.models import User


def send_letter(inn: str, name: str, phone: str, email: str) -> None:
    theme = 'Зарегистрирован новый клиент в системе "Портал разработки"'
    message = f'Зарегистрирован новый клиент:\n' \
              f'ИНН: {inn}\n' \
              f'Организация: {name}\n' \
              f'Телефон: {phone}\n' \
              f'e-mail: {email}\n\n' \
              f'Создано: {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}\n'
    if settings.CELERY_BROKER_URL:
        send_new_email.delay(
            settings.EMAIL_ADR_REGISTRATION,
            theme,
            message
        )
    else:
        send_new_letter(
            settings.EMAIL_ADR_REGISTRATION,
            theme,
            message
        )


def send_token(new_pass: str, email: str, confirm_link: str) -> None:
    message = _(f"Follow this link %s \n"
                f"to confirm! \n" % confirm_link)
    theme = _('New client registered in Development Portal')

    if new_pass:
        message += f"Your new password {new_pass} \n "
    if settings.CELERY_BROKER_URL:
        send_new_email.delay(
            email,
            theme,
            message
        )
    else:
        send_new_letter(
            email,
            theme,
            message
        )
