from typing import Dict

from django.conf import settings
from django.core.mail import EmailMultiAlternatives,get_connection
from django.template.loader import render_to_string

from core.tasks import send_mail_task


class BaseEmail:
    template_name = ""
    subject = ""

    def send_mail(
        self, recipient_list: list, data: dict = {}, subject: str = ""
    ) -> int:
        if not subject:
            subject = self.subject
        content = render_to_string(self.template_name, data)
        return send_mail_task.delay(
            subject=subject,
            message="",
            html_message=content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
        )

    def send_mass_mail(self, data: Dict[str, Dict]):
        """
        Accept data email as key and data as value.
        """
        messages = []
        for email, datum in data.items():
            content = render_to_string(
                self.template_name,
                datum,
            )
            message = EmailMultiAlternatives(
                self.subject,
                "",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            message.attach_alternative(content, "text/html")
            messages.append(message)
        connection = get_connection()
        connection.send_messages(messages)
