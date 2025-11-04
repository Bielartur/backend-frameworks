from ninja import Schema
from pydantic import EmailStr


class CadastrarIn(Schema):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class LoginIn(Schema):
    email: EmailStr
    password: str


class SlidingOut(Schema):
    token: str
