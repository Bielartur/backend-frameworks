from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from core.auth import jwt_auth
from core.schemas import ErrorSchema
from contas.services import auth_services as services
from contas.schemas.auth_schema import TokenResponse, LoginIn, CadastrarIn

auth_router = Router(tags=["Autenticação"])


# LOGIN (Sliding) -> POST /autenticacao/login
@auth_router.post("/login", response={200: TokenResponse, 401: ErrorSchema})
def login(request: HttpRequest, payload: LoginIn):
    """
    Endpoint de login que autentica o usuário e retorna um sliding token.
    O usuário deve ser autenticado usando email e senha.
    """
    usuario = services.autenticar_usuario(payload)

    # Gera o sliding token para o usuário autenticado
    sliding_token = services.gerar_token(usuario)

    return {
        "message": "Login efetuado com sucesso!",
        "data": {"token": str(sliding_token), "usuario": usuario},
    }


# CADASTRO (Sliding) -> POST /autenticacao/cadastro
@auth_router.post("/cadastro", response={200: TokenResponse, 401: ErrorSchema})
def cadastro(request: HttpRequest, payload: CadastrarIn):
    """
    Endpoint de cadastro que cria um novo usuário e retorna um sliding token.
    Se o email já existir, retorna um erro.
    """

    # Verfica se o email já está associado à outra conta
    services.validar_email_disponivel(payload.email)
    usuario = services.usuario_save(payload)

    # Gera o sliding token para o novo usuário
    sliding_token = services.gerar_token(usuario)

    return {
        "message": "Usuário cadastrado com sucesso!",
        "data": {"token": str(sliding_token), "usuario": usuario},
    }


@auth_router.get(
    "/atualizar_token", response={200: TokenResponse, 401: ErrorSchema}, auth=jwt_auth
)
def atualizar_token(request):
    token_str = request.headers.get("Authorization", "").replace("Bearer ", "")
    novo_token = services.atualizar_token(token_str)
    if novo_token:
        request.token = novo_token
        return {
            "message": "Token atualizado com sucesso!",
            "data": {"token": novo_token, "usuario": request.user},
        }
    else:
        raise HttpError(401, "Token inválido ou expirado")
