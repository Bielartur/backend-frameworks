from ninja import Schema
from pydantic import EmailStr
from typing import Optional

class CadastrarIn(Schema):
    first_name: str
    last_name: Optional[str | None] = None
    email: EmailStr
    password: str
    password_confirm: str


class LoginIn(Schema):
    email: EmailStr
    password: str


class UsuarioSchema(Schema):
    id: int
    first_name: str
    last_name: Optional[str | None] = None
    email: EmailStr


class SlidingOut(Schema):
    token: str
    usuario: UsuarioSchema

class AtualizarTokenOut(Schema):
    detail: str
    token: str