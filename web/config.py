import os
from web.db import get_db_session
from flask import Flask
from dotenv import load_dotenv

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
    app.session = get_db_session(env)
    return app


app = create_app()
