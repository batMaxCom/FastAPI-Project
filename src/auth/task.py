import smtplib
from email.message import EmailMessage

# from celery import Celery

from src.config import SMTP_PASSWORD, SMTP_USER

SMTP_HOST = "smtp.mail.ru"
SMTP_PORT = 465

# tasks - название(любое)
# broker - узказывается брокер задач
# celery = Celery('tasks', broker='redis://localhost:6379')


def get_email_template_dashboard(username: str, user_email: str, code: int):
    email = EmailMessage()
    email['Subject'] = 'Натрейдил Отчет Дашборд'
    email['From'] = SMTP_USER
    email['To'] = user_email
    email.set_content(f'Hello {username}. You code {code}')
    return email

# задачи Celery оборачиваются в декоратор с именем переменной, заданной классом Celery
# @celery.task
def send_email_report_dashboard(username: str, email: str, code: int):
    email = get_email_template_dashboard(username, email, code)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
