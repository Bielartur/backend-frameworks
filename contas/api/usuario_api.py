from ninja import Router
from django.contrib.auth import get_user_model

from contas.schemas.auth_schema import UsuarioSchema
from core.auth import jwt_auth

User = get_user_model()
router = Router(tags=["Usuário"])


@router.get(
    "/perfil",
    auth=jwt_auth,
    summary="Dados do próprio usuário autenticado",
    response=UsuarioSchema,
)
def eu(request):
    return request.user
