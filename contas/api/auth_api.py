# api.py
from ninja import Router
from ninja.errors import HttpError
from ninja_jwt.tokens import SlidingToken
from django.contrib.auth import get_user_model, authenticate
from django.http import HttpRequest

from contas.schemas.auth_schema import SlidingOut, LoginIn, CadastrarIn

User = get_user_model()
auth_router = Router(tags=["Autenticação"])


# LOGIN (Sliding) -> POST /api/autenticacao/login
@auth_router.post("/login", response=SlidingOut)
def login(request: HttpRequest, data: LoginIn):
    """
    Endpoint de login que autentica o usuário e retorna um sliding token.
    O usuário deve ser autenticado usando email e senha.
    """
    # Autentica usando email (que é o USERNAME_FIELD do modelo Usuario)
    user = authenticate(username=data.email, password=data.password)

    if not user:
        raise HttpError(401, "Usuário e/ou senha incorreto(s)")
    
    # Gera o sliding token para o usuário autenticado
    sliding_token = SlidingToken.for_user(user)
    
    return SlidingOut(token=str(sliding_token))


# CADASTRO (Sliding) -> POST /api/autenticacao/cadastro
@auth_router.post("/cadastro", response=SlidingOut)
def cadastro(request: HttpRequest, data: CadastrarIn):
    """
    Endpoint de cadastro que cria um novo usuário e retorna um sliding token.
    Se o email já existir, retorna um erro.
    """
    # Verifica se o email já está cadastrado
    if User.objects.filter(email=data.email).exists():
        raise HttpError(400, "Este email já está cadastrado")
    
    # Cria o novo usuário
    user = User.objects.create_user(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=data.password
    )
    
    # Gera o sliding token para o novo usuário
    sliding_token = SlidingToken.for_user(user)
    
    return SlidingOut(token=str(sliding_token))

