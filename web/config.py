import os
from web.db import get_db_session
from flask import Flask
from dotenv import load_dotenv
from flask_mail import Mail

load_dotenv()

env = {
    "database": {
        "host": os.environ["HOST"],
        "port": os.environ["PORT"],
        "user": os.environ["DBUSER"],
        "password": os.environ["DB_PASSWORD"],
        "dbname": os.environ["DBNAME"],
        "schema": os.environ["SCHEMA"].lower(),
    },
    "secret_key": os.environ["SECRET_KEY"],
    "debug": os.environ["DEBUG"],
}


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.session = get_db_session(env)
    return app


MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# gmail authentication
MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']

# mail accounts
MAIL_DEFAULT_SENDER = 'abhishek.kaushik16400@gmail.com'

app = create_app()
mail = Mail(app)
