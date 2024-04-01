import smtplib
from email.mime.text import MIMEText

from app.core.env import SMTP_HOST, SMTP_PORT


class MailService:
    def __init__(self, smtp_host: str = SMTP_HOST, smtp_port: int = SMTP_PORT):
        self.__smtp_host = smtp_host
        self.__smtp_port = smtp_port

    async def send_mail(self, subject: str, body: str, from_email: str, to_email: str):
        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = from_email
        message["To"] = to_email

        server = smtplib.SMTP(self.__smtp_host, self.__smtp_port)
        server.send_message(message)
        server.quit()
