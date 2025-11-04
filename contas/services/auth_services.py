from ninja_jwt.tokens import SlidingToken, Token
from django.contrib.auth import authenticate
from ninja.errors import HttpError
from pydantic import EmailStr

from contas.models import Usuario
from contas.schemas.auth_schema import LoginIn, CadastrarIn


def autenticar_usuario(payload: LoginIn) -> Usuario:
    """
    Autentica usando email (que é o USERNAME_FIELD do modelo Usuario)
    """
    usuario = authenticate(username=payload.email, password=payload.password)

    if not usuario:
        raise HttpError(401, "Usuário e/ou senha incorreto(s)")
    
    return usuario

def validar_email_disponivel(email: EmailStr) -> None:
    """
    Lança HttpError(400) se o e-mail já estiver cadastrado.
    """
    if Usuario.objects.filter(email=email).exists():
        raise HttpError(400, "Este e-mail já está cadastrado")

def usuario_save(payload: CadastrarIn) -> Usuario:
    # Cria o novo usuário
    usuario = Usuario.objects.create_user(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        password=payload.password
    )

    return usuario

def gerar_token(usuario: Usuario) -> Token:
    return SlidingToken.for_user(usuario)