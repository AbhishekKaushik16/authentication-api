import os

from flask_mail import Mail, Message

from web.config import mail
from dotenv import load_dotenv
load_dotenv()

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=os.environ.get('MAIL_DEFAULT_SENDER')
    )
    mail.send(msg)
