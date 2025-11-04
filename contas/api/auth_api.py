from django.http import HttpRequest
from ninja import Router

from core.schemas import ErrorSchema
from contas.services import auth_services as services
from contas.schemas.auth_schema import SlidingOut, LoginIn, CadastrarIn
from contas.services.auth_services import validar_email_disponivel

auth_router = Router(tags=["Autenticação"])


# LOGIN (Sliding) -> POST /autenticacao/login
@auth_router.post("/login", response={200: SlidingOut, 401: ErrorSchema})
def login(request: HttpRequest, payload: LoginIn):
    """
    Endpoint de login que autentica o usuário e retorna um sliding token.
    O usuário deve ser autenticado usando email e senha.
    """
    usuario = services.autenticar_usuario(payload)
    
    # Gera o sliding token para o usuário autenticado
    sliding_token = services.gerar_token(usuario)
    
    return SlidingOut(token=str(sliding_token))


# CADASTRO (Sliding) -> POST /autenticacao/cadastro
@auth_router.post("/cadastro", response={200: SlidingOut, 401: ErrorSchema})
def cadastro(request: HttpRequest, payload: CadastrarIn):
    """
    Endpoint de cadastro que cria um novo usuário e retorna um sliding token.
    Se o email já existir, retorna um erro.
    """

    # Verfica se o email já está associado à outra conta
    validar_email_disponivel(payload.email)
    usuario = services.usuario_save(payload)
    
    # Gera o sliding token para o novo usuário
    sliding_token = services.gerar_token(usuario)
    
    return SlidingOut(token=str(sliding_token))

