from datetime import datetime

from apps.clients.tasks import send_new_email
from utils.email import send_new_letter

from settings import settings


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
