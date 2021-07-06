import os

from flask import url_for, render_template
from flask_mail import Message

from api.utils.helpers import generate_confirmation_token
from web.config import mail
from dotenv import load_dotenv
load_dotenv()

def send_email_confirm_mail(user):
    token = generate_confirmation_token(user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    msg = Message(
        subject,
        recipients=[user.email],
        html=html,
        sender=os.environ.get('MAIL_DEFAULT_SENDER')
    )
    mail.send(msg)

def send_password_change_mail(user):
    try:
        token = generate_confirmation_token(user.email)
        password_reset_form_url = url_for('password_reset_form', token=token, _external=True)
        html = render_template('password_reset_link.html', password_reset_form_url=password_reset_form_url)
        subject = "Please follow this url to change your password"
        msg = Message(
            subject,
            recipients=[user.email],
            html=html,
            sender=os.environ.get('MAIL_DEFAULT_SENDER')
        )
        mail.send(msg)
        response_object = {
            'status': 'success',
            'email': user.email
        }
        return response_object, 200
    except Exception as exc:
        print(exc)
        response_object = {
            'status': 'fail',
            'message': str(exc)
        }
        return response_object, 500

def send_password_reset_link(email: str):
    token = generate_confirmation_token(email)
    password_change_url = url_for('password_reset', token=token, _external=True)
    return render_template('password_change_form.html', password_change_url=password_change_url)
