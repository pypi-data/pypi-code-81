import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, Optional, Type, Union

from flask import Flask
from jinja2 import Environment, FileSystemLoader

from .utils_email import parse_email_url

email_log = logging.getLogger('fittrackee_api_email')
email_log.setLevel(logging.DEBUG)


class EmailMessage:
    def __init__(
        self, sender: str, recipient: str, subject: str, html: str, text: str
    ) -> None:
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.html = html
        self.text = text

    def generate_message(self) -> MIMEMultipart:
        message = MIMEMultipart('alternative')
        message['Subject'] = self.subject
        message['From'] = self.sender
        message['To'] = self.recipient
        part1 = MIMEText(self.text, 'plain')
        part2 = MIMEText(self.html, 'html')
        message.attach(part1)
        message.attach(part2)
        return message


class EmailTemplate:
    def __init__(self, template_directory: str) -> None:
        self._env = Environment(loader=FileSystemLoader(template_directory))

    def get_content(
        self, template_name: str, lang: str, part: str, data: Dict
    ) -> str:
        template = self._env.get_template(f'{template_name}/{lang}/{part}')
        return template.render(data)

    def get_all_contents(self, template: str, lang: str, data: Dict) -> Dict:
        output = {}
        for part in ['subject.txt', 'body.txt', 'body.html']:
            output[part] = self.get_content(template, lang, part, data)
        return output

    def get_message(
        self, template: str, lang: str, sender: str, recipient: str, data: Dict
    ) -> MIMEMultipart:
        output = self.get_all_contents(template, lang, data)
        message = EmailMessage(
            sender,
            recipient,
            output['subject.txt'],
            output['body.html'],
            output['body.txt'],
        )
        return message.generate_message()


class Email:
    def __init__(self, app: Optional[Flask] = None) -> None:
        self.host = 'localhost'
        self.port = 1025
        self.use_tls = False
        self.use_ssl = False
        self.username = None
        self.password = None
        self.sender_email = 'no-reply@example.com'
        self.email_template: Optional[EmailTemplate] = None
        if app is not None:
            self.init_email(app)

    def init_email(self, app: Flask) -> None:
        parsed_url = parse_email_url(app.config['EMAIL_URL'])
        self.host = parsed_url['host']
        self.port = parsed_url['port']
        self.use_tls = parsed_url['use_tls']
        self.use_ssl = parsed_url['use_ssl']
        self.username = parsed_url['username']
        self.password = parsed_url['password']
        self.sender_email = app.config['SENDER_EMAIL']
        self.email_template = EmailTemplate(app.config['TEMPLATES_FOLDER'])

    @property
    def smtp(self) -> Type[Union[smtplib.SMTP_SSL, smtplib.SMTP]]:
        return smtplib.SMTP_SSL if self.use_ssl else smtplib.SMTP

    def send(
        self, template: str, lang: str, recipient: str, data: Dict
    ) -> None:
        if not self.email_template:
            raise Exception('No email template defined.')
        message = self.email_template.get_message(
            template, lang, self.sender_email, recipient, data
        )
        connection_params = {}
        if self.use_ssl or self.use_tls:
            context = ssl.create_default_context()
        if self.use_ssl:
            connection_params.update({'context': context})
        with self.smtp(
            self.host, self.port, **connection_params  # type: ignore
        ) as smtp:
            smtp.login(self.username, self.password)  # type: ignore
            if self.use_tls:
                smtp.starttls(context=context)
            smtp.sendmail(self.sender_email, recipient, message.as_string())
            smtp.quit()
