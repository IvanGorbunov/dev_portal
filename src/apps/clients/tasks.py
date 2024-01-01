from celery import shared_task

from utils.email import send_new_letter
from settings.celery import app


@app.task
def send_new_email(email: str, theme: str, message: str):
    send_new_letter(email, theme, message)


@shared_task
def bar():
    return 'Hello world!'