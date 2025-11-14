from ninja_jwt.exceptions import TokenError, InvalidToken
from ninja_jwt.tokens import SlidingToken, Token
from django.contrib.auth import authenticate
from ninja.errors import HttpError
from pydantic import EmailStr

from contas.models import Usuario
from contas.schemas.auth_schema import LoginIn, CadastrarIn


def get_usuario_by_id(request, usuario_id: int) -> Usuario | None:
    try:
        return Usuario.objects.get(pk=usuario_id)
    except Usuario.DoesNotExist:
        raise HttpError(404, f"Usuario de ID {usuario_id} não encontrado")


def get_usuario_atual(request) -> Usuario | None:
    # Caso esteja autenticado normalmente (ex: Session ou JWTUser)
    if hasattr(request, "user") and request.user and request.user.is_authenticated:
        return request.user

    # Caso o user não esteja em request.user mas o token JWT contenha info
    if hasattr(request, "auth") and request.auth:

        # Exemplo: se request.auth for um dict com o ID do usuário
        if isinstance(request.auth, dict) and "user_id" in request.auth:
            return Usuario.objects.filter(id=request.auth["user_id"]).first()

        # Caso já seja um objeto do modelo Usuario
        elif isinstance(request.auth, Usuario):
            return request.auth

    # Se não achar ninguém, pode retornar None ou levantar exceção
    return None


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
        raise HttpError(409, "Este e-mail já está cadastrado")


def usuario_save(payload: CadastrarIn) -> Usuario:
    if not payload.password == payload.password_confirm:
        raise HttpError(400, "As senhas não conferem. Tente novamente.")

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


def atualizar_token(token_str: str):
    try:
        # Verifica se o token é válido e dentro do refresh_exp
        token = SlidingToken(token_str)
        token.check_exp()  # valida expiração
        token.set_exp()  # define novo exp (renova a validade)
        return str(token)
    except (TokenError, InvalidToken):
        return None
