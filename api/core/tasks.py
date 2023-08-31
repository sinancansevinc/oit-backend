from smtplib import SMTPDataError
from typing import List

import requests
from django.core.mail import send_mail

from oit_backend.celery import app

@app.task(
    autoretry_for=(SMTPDataError,), retry_kwargs={"max_retries": 5, "countdown": 60}
)
def send_mail_task(
    subject: str,
    message: str,
    html_message: str,
    from_email: str,
    recipient_list: List[str],
):
    return send_mail(
        subject=subject,
        message=message,
        html_message=html_message,
        from_email=from_email,
        recipient_list=recipient_list,
    )
