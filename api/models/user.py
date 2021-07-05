# coding: utf-8
import jwt
import os
import datetime
import bcrypt
from dotenv import load_dotenv
from .base import base_object, userMixin
from sqlalchemy import Column, Text, Boolean, Float
from ..utils.helpers import get_current_time

load_dotenv()


class User(base_object, userMixin):
    __tablename__ = "user"

    name = Column(Text, nullable=False)
    email = Column(Text, unique=True)
    address = Column(Text)
    id = Column(Text, primary_key=True)
    passwordHash = Column(Text, nullable=False)
    emailVerified = Column(Boolean)
    photoUrl = Column(Text)
    passwordUpdatedAt = Column(Float(53))
    disabled = Column(Boolean)
    lastLoginAt = Column(Text)
    createdAt = Column(Text)

    def __init__(self, d: dict):
        self.name = d.get("name", None)
        self.id = d.get("id", None)
        self.address = d.get("address", None)
        self.email = d.get("email", None)
        self.passwordHash = (
            bcrypt.hashpw(
                str(d.get("password")).encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            if d.get("password")
            else None
        )
        self.emailVerified = d.get("emailVerified", None)
        self.photoUrl = d.get("photoUrl", None)
        self.disabled = d.get("disabled", None)
        self.createdAt = d.get("createdAt", None)
        self.lastLoginAt = d.get("lastLoginAt", None)
        self.passwordUpdatedAt = d.get("passwordUpdateAt", None)

    def encode_auth_token(self, days=0, hours=1, minutes=0, seconds=0):
        try:
            payload = {
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(
                    days=days, hours=hours, minutes=minutes, seconds=seconds
                ),
                "iat": datetime.datetime.utcnow(),
                "sub": {"id": self.id},
            }
            return jwt.encode(payload, os.environ.get("SECRET_KEY"), algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, os.environ.get("SECRET_KEY"))
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."


import uuid


def register_user(client, post_data):
    session = client.session_factory()
    client._set_schema(session)
    user = session.query(User).filter_by(email=post_data["email"]).first()
    if not user:
        try:
            post_data["id"] = str(uuid.uuid4())
            user = User(post_data)
            user.lastLoginAt = user.createdAt = get_current_time()
            user.emailVerified = False
            session.add(user)
            session.commit()
            auth_token = user.encode_auth_token(hours=2)
            response_object = {
                "status": "success",
                "message": "Successfully registered",
                "auth_token": auth_token,
                "expiresIn": str(2 * 60 * 60),
                "id": user.id,
            }
            return response_object, 201
        except Exception as exc:
            print(exc)
            session.rollback()
            response_object = {
                "status": "fail",
                "message": str(exc),
            }
            return response_object, 401
    else:
        response_object = {
            "status": "fail",
            "message": "User already exists. Please Log in",
        }
        return response_object, 202


def login_user(client, post_data):
    session = client.session_factory()
    client._set_schema(session)
    try:
        user = session.query(User).filter_by(email=post_data.get("email")).first()
        if user and bcrypt.checkpw(
            post_data.get("password").encode("utf-8"), user.passwordHash.encode("utf-8")
        ):
            user.lastLoginAt = get_current_time()
            session.commit()
            auth_token = user.encode_auth_token(hours=1)
            response_object = {
                "status": "success",
                "message": "Successfully Logged in.",
                "auth_token": auth_token,
                "expiresIn": str(1 * 60 * 60),
                "id": user.id,
            }
            return response_object, 200
        else:
            response_object = {"status": "fail", "message": "User does not exist."}
            return response_object, 404
    except Exception as exc:
        session.rollback()
        print(exc)
        response_object = {"status": "fail", "message": str(exc)}
        return response_object, 500
