from functools import wraps
import jwt
import os
import datetime
from flask import abort, request
from dotenv import load_dotenv

load_dotenv()


def check_token(f):
    @wraps(f)
    def authorize(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)
        user = None
        data = request.headers["Authorization"]
        token = str.replace(str(data), "Bearer ", "")
        try:
            user_id = jwt.decode(
                token, os.environ.get("SECRET_KEY"), algorithms=["HS256"]
            )["sub"]
        except Exception as exc:
            abort(401)
        return f(*args, **kwargs)

    return authorize
